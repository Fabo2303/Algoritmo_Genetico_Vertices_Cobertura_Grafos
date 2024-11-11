import random
from utilz import create_title, create_cells, create_output_file

celdas = []

# Inicialización de la población
def inicializar_poblacion(tamanio, grafo):
    poblacion = []
    vertices = list(grafo.keys())
    celdas.append(create_title("POBLACIÓN INICIAL"))
    for j in range(tamanio):
        celdas.append("Individuo #" + str(j + 1) + "\n")
        individuo = {v: random.choice([0, 1]) for v in
                     vertices}  # 1 indica que el vértice está en el conjunto de cobertura
        celdas.extend(create_cells(individuo))
        poblacion.append(individuo)
    return poblacion


# Función de aptitud compatible con grafos dirigidos y no dirigidos
def evaluar_aptitud_general(individuo, grafo, dirigido=False, torneo=False):
    cubre_aristas = set()
    for v, estado in individuo.items():
        if estado == 1:  # El vértice está en el conjunto de cobertura
            for destino in grafo[v]:  # Agregar todas las aristas que salen de 'v'
                if dirigido:
                    cubre_aristas.add((v, destino))  # Para grafos dirigidos
                else:
                    # Para grafos no dirigidos, añadir arista en ambas direcciones
                    cubre_aristas.add((min(v, destino), max(v, destino)))

    total_aristas = sum(len(destinos) for destinos in grafo.values()) // (1 if dirigido else 2)
    aristas_cubiertas = len(cubre_aristas)
    num_vertices_cubriendo = sum(individuo.values())
    if torneo:
        celdas.append("Aristas Cubiertas: ")
        for arista in cubre_aristas:
            celdas.append(str(arista) + " ")
        celdas.append("\nAptitud: ")

    if aristas_cubiertas < total_aristas:
        if torneo:
            celdas.append("-1\n\n")
        return -1  # Penalización si no cubre todas las aristas
    else:
        if torneo:
            celdas.append(str(total_aristas / num_vertices_cubriendo) + "\n\n")
        return total_aristas / num_vertices_cubriendo  # Mejor puntaje para menos vértices


# Selección de padres
def seleccion_por_torneo(poblacion, grafo, dirigido):
    torneo = random.sample(poblacion, 3)
    celdas.append("Muestras\n")
    for i in range(3):
        celdas.append("Muestra #" + str(i + 1) + "\n")
        celdas.extend(create_cells(torneo[i]))
        evaluar_aptitud_general(torneo[i], grafo, dirigido, torneo = True)

    torneo.sort(key=lambda ind: evaluar_aptitud_general(ind, grafo, dirigido), reverse=True)
    celdas.append("Padre seleccionado\n")
    celdas.extend(create_cells(torneo[0]))
    return torneo[0]


# Cruce de dos individuos
def cruce(padre1, padre2):
    hijo = {}
    for gen in padre1:
        ran = random.random() < 0.5
        if ran:
            celdas.append("Gen #" + str(gen) + " de Padre #1\n")
        else:
            celdas.append("Gen #" + str(gen) + " de Padre #2\n")
        hijo[gen] = padre1[gen] if ran else padre2[gen]
    return hijo


# Mutación
def mutacion(individuo, prob_mutacion):
    for gen in individuo:
        if random.random() < prob_mutacion:
            celdas.append("Gen #" + str(gen) + " mutado\n")
            individuo[gen] = 1 - individuo[gen]  # Cambia entre 0 y 1
    celdas.append("Individuo mutado\n")
    celdas.extend(create_cells(individuo))
    return individuo


# Algoritmo genético principal
def algoritmo_genetico(grafo, tam_poblacion, generaciones, prob_mutacion, dirigido=False):
    poblacion = inicializar_poblacion(tam_poblacion, grafo)

    for _ in range(generaciones):
        nueva_poblacion = []
        for _ in range(tam_poblacion // 2):
            celdas.append(create_title("SELECCIÓN POR TORNEO"))
            celdas.append("Padre #1\n")
            padre1 = seleccion_por_torneo(poblacion, grafo, dirigido)
            celdas.append("Padre #2\n")
            padre2 = seleccion_por_torneo(poblacion, grafo, dirigido)
            celdas.append(create_title("CRUCE"))

            celdas.append("Padre #1\n")
            celdas.extend(create_cells(padre1))
            celdas.append("Padre #2\n")
            celdas.extend(create_cells(padre2))
            celdas.append("Hijo #1\n")
            hijo1 = cruce(padre1, padre2)
            celdas.extend(create_cells(hijo1))

            celdas.append("Hijo #2\n")
            hijo2 = cruce(padre1, padre2)
            celdas.extend(create_cells(hijo2))

            celdas.append(create_title("MUTACIÓN"))
            celdas.append("Hijo #1\n")
            hijo1 = mutacion(hijo1, prob_mutacion)
            celdas.append("Hijo #2\n")
            hijo2 = mutacion(hijo2, prob_mutacion)

            nueva_poblacion.extend([hijo1, hijo2])

        celdas.append(create_title("NUEVA POBLACIÓN"))
        # Reemplazar la población antigua
        poblacion = sorted(nueva_poblacion, key=lambda ind: evaluar_aptitud_general(ind, grafo, dirigido), reverse=True)

        for i in range(tam_poblacion):
            celdas.append("Individuo #" + str(i + 1) + "\n")
            celdas.extend(create_cells(poblacion[i]))

        # Guardar y mostrar el mejor individuo de cada generación
        mejor_individuo = poblacion[0]

        celdas.append(create_title("MEJOR SOLUCIÓN DE LA GENERACIÓN"))
        celdas.extend(create_cells(mejor_individuo))
        evaluar_aptitud_general(mejor_individuo, grafo, dirigido, torneo=True)
        print("Mejor solución de la generación:", mejor_individuo, " Aptitud:",
              evaluar_aptitud_general(mejor_individuo, grafo, dirigido))

    celdas.append(create_title("MEJOR SOLUCIÓN"))
    celdas.extend(create_cells(mejor_individuo))
    evaluar_aptitud_general(mejor_individuo, grafo, dirigido, torneo=True)
    create_output_file(celdas)
    celdas.clear()
    return mejor_individuo
