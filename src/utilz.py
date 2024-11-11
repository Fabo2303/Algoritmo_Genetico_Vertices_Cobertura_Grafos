import networkx as nx
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

G = None
pos = None
icons = {
    "1": "─",
    "2": "┬",
    "3": "┌",
    "4": "│",
    "5": "┐",
    "6": "┴",
    "7": "└",
    "8": "┘",
    "9": " "
}

def dibujar_grafo(grafo, dirigido, nombre="files/grafo.png", solution=None, close=True):
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
    with open("files/grafos.txt", "r") as archivo:
        for linea in archivo:
            diccionario, dirigido = map(eval, linea.strip().split(";"))
            grafos.append((diccionario, dirigido))

    return grafos


def create_file():
    with open("files/output.txt", "w") as file:
        file.write("")
        file.close()


def write_file(line):
    with open("files/output.txt", "w") as file:
        file.write(line)
        file.close()


def delete_file():
    with open("files/output.txt", "w") as file:
        file.write("")
        file.close()


def generate_cells(vertices):
    cells = []
    n = len(vertices)
    keys = list(vertices.keys())
    values = list(vertices.values())
    for i in range(0, 5):
        if i == 0:
            for key, _ in enumerate(keys):
                cells.append(icons["9"] * 3)
                cells.append(str(key))
                cells.append(icons["9"] * 2)
        if i == 1:
            for j, key in enumerate(keys):
                if j == 0:
                    cells.append(icons["3"])
                    cells.append(icons["1"] * 5)
                else:
                    cells.append(icons["2"])
                    cells.append(icons["1"] * 5)
                if j == n - 1:
                    cells.append(icons["5"])
        if i == 2:
            for j, value in enumerate(values):
                if j == 0:
                    cells.append(icons["4"])
                    cells.append(icons["9"] * 2)
                    cells.append(str(value))
                    cells.append(icons["9"] * 2)
                else:
                    cells.append(icons["4"])
                    cells.append(icons["9"] * 2)
                    cells.append(str(value))
                    cells.append(icons["9"] * 2)
                if j == n - 1:
                    cells.append(icons["4"])
        if i == 3:
            for j, key in enumerate(keys):
                if j == 0:
                    cells.append(icons["7"])
                    cells.append(icons["1"] * 5)
                else:
                    cells.append(icons["6"])
                    cells.append(icons["1"] * 5)
                if j == n - 1:
                    cells.append(icons["8"])
        cells.append("\n")

    return cells

def create_title(title):
    return icons["1"]*8 + title + icons["1"]*8 + "\n\n"

def create_cells(individuo):
    celdas = generate_cells(individuo)
    return celdas

def create_output_file(celdas):
    delete_file()
    write_file("".join(celdas))
    txt_to_pdf("files/output.txt", "files/output.pdf")


def txt_to_pdf(input_txt_path, output_pdf_path):
    # Configuración del lienzo y página
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    y_position = height - 40  # Posición inicial en y

    # Registrar la fuente monoespaciada
    pdfmetrics.registerFont(TTFont("DejaVuSansMono", "resources/DejaVuSansMono.ttf"))  # Cambia a la ruta de tu archivo .ttf
    c.setFont("DejaVuSansMono", 10)  # Ajusta el tamaño de la fuente a 10 (monoespaciada)

    # Leer el archivo de texto y agregar contenido al PDF línea por línea
    with open(input_txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Dibuja la línea de texto tal como está, respetando espacios
            c.drawString(40, y_position, line.rstrip())  # `rstrip` para eliminar espacios solo al final de la línea
            y_position -= 12  # Espaciado entre líneas
            if y_position < 40:  # Nueva página si se alcanza el final de la página actual
                c.showPage()
                c.setFont("DejaVuSansMono", 10)  # Restablece la fuente en la nueva página
                y_position = height - 40

    c.save()
    print(f"Archivo PDF generado: {output_pdf_path}")
