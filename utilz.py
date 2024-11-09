import networkx as nx
import matplotlib.pyplot as plt

G = None
pos = None

def dibujar_grafo(grafo, dirigido, nombre="grafo.png", solution=None, close=True):
    global G
    global pos

    if close:
        G = None
        pos = None

    if G is None:
        G = nx.DiGraph() if dirigido else nx.Graph()
        for vertice, destinos in grafo.items():
            for destino in destinos:
                G.add_edge(vertice, destino)

        # Diseño del grafo y personalización
        pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    if dirigido:
        nx.draw_networkx_edges(G, pos, edge_color="gray", width=2, arrows=True, arrowstyle='-|>', arrowsize=20)
    else:
        nx.draw_networkx_edges(G, pos, edge_color="gray", width=2)

    if solution is not None:
        nodos = [v for v, estado in solution.items() if estado == 1]
        nx.draw_networkx_nodes(G, pos, nodelist=nodos, node_size=700, node_color="red")
        plt.title("Solución encontrada")
        plt.savefig(nombre)
    else:
        plt.title("Grafo seleccionado")
        plt.savefig(nombre)

    plt.clf()
    plt.close()


def lector():
    grafos = []
    with open("grafos.txt", "r") as archivo:
        for linea in archivo:
            diccionario, dirigido = map(eval, linea.strip().split(";"))
            grafos.append((diccionario, dirigido))

    return grafos