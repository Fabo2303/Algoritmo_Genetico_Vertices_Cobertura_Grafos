import random


# Inicialización de la población
def inicializar_poblacion(tamanio, grafo):
    poblacion = []
    vertices = list(grafo.keys())
    for _ in range(tamanio):
        individuo = {v: random.choice([0, 1]) for v in
                     vertices}  # 1 indica que el vértice está en el conjunto de cobertura
        poblacion.append(individuo)
    return poblacion


# Función de aptitud compatible con grafos dirigidos y no dirigidos
def evaluar_aptitud_general(individuo, grafo, dirigido=False):
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

    if aristas_cubiertas < total_aristas:
        return -1  # Penalización si no cubre todas las aristas
    else:
        return total_aristas / num_vertices_cubriendo  # Mejor puntaje para menos vértices


# Selección de padres
def seleccion_por_torneo(poblacion, grafo, dirigido):
    torneo = random.sample(poblacion, 3)
    torneo.sort(key=lambda ind: evaluar_aptitud_general(ind, grafo, dirigido), reverse=True)
    return torneo[0]


# Cruce de dos individuos
def cruce(padre1, padre2):
    hijo = {}
    for gen in padre1:
        hijo[gen] = padre1[gen] if random.random() < 0.5 else padre2[gen]
    return hijo


# Mutación
def mutacion(individuo, prob_mutacion):
    for gen in individuo:
        if random.random() < prob_mutacion:
            individuo[gen] = 1 - individuo[gen]  # Cambia entre 0 y 1
    return individuo


# Algoritmo genético principal
def algoritmo_genetico(grafo, tam_poblacion, generaciones, prob_mutacion, dirigido=False):
    poblacion = inicializar_poblacion(tam_poblacion, grafo)

    for _ in range(generaciones):
        nueva_poblacion = []
        for _ in range(tam_poblacion // 2):
            padre1 = seleccion_por_torneo(poblacion, grafo, dirigido)
            padre2 = seleccion_por_torneo(poblacion, grafo, dirigido)
            hijo1 = cruce(padre1, padre2)
            hijo2 = cruce(padre1, padre2)
            hijo1 = mutacion(hijo1, prob_mutacion)
            hijo2 = mutacion(hijo2, prob_mutacion)
            nueva_poblacion.extend([hijo1, hijo2])

        # Reemplazar la población antigua
        poblacion = sorted(nueva_poblacion, key=lambda ind: evaluar_aptitud_general(ind, grafo, dirigido), reverse=True)

        # Guardar y mostrar el mejor individuo de cada generación
        mejor_individuo = poblacion[0]
        print("Mejor solución de la generación:", mejor_individuo, " Aptitud:",
              evaluar_aptitud_general(mejor_individuo, grafo, dirigido))

    return mejor_individuo