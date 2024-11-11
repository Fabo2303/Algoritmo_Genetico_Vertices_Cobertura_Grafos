import tkinter as tk
from PIL import Image, ImageTk

from src.algoritmo_genetico import algoritmo_genetico
from src.utilz import dibujar_grafo, lector

grafos = []
grafo_seleccionado = []


def add_title(name):
    title = tk.Label(root, text=name, font=("Arial", 20), bg="black", fg="white")
    title.pack()


def add_input(name, x_label, y_label, x_entry, y_entry):
    input_label = tk.Label(root, text=name, font=("Arial", 16), bg="black", fg="white", width=20, height=2)
    input_label.place(x=x_label, y=y_label)
    input_entry = tk.Entry(root, bg="white", fg="black", width=20, font=("Arial", 16))
    input_entry.place(x=x_entry, y=y_entry)
    return input_entry

def add_button(name, event, action, x_label, y_label):
    button_item = tk.Button(root, text=name, bg="lightblue", fg="black", font=("Arial", 16), width=18, height=1)
    button_item.place(x=x_label, y=y_label)
    button_item.bind(event, action)
    return button_item

def add_select_graph(event, action, x_label, y_label):
    select_item = tk.Listbox(root, bg="white", fg="black", font=("Arial", 16), width=20, height=5)
    select_item.place(x=x_label, y=y_label)
    for i, (grafo, dirigido) in enumerate(grafos):
        select_item.insert(i, f"Grafo {i + 1} - {'dirigido' if dirigido else 'no dirigido'}")
    select_item.bind(event, action)
    return select_item


def add_image_selected(grafo, name, solution=None, close=True):
    global grafo_seleccionado
    grafo_seleccionado = grafo
    dibujar_grafo(grafo[0], grafo[1], name, solution, close)
    img = Image.open(name)  # Abre la imagen con PIL
    img = img.resize((500, 500))  # Redimensiona la imagen si es necesario
    tk_img = ImageTk.PhotoImage(img)  # Convierte la imagen para Tkinter
    # Crea el widget de etiqueta o actualiza la imagen si ya existe
    if hasattr(add_image_selected, "label"):
        add_image_selected.label.configure(image=tk_img)
        add_image_selected.label.image = tk_img  # Mantiene la referencia
    else:
        add_image_selected.label = tk.Label(root, image=tk_img)
        add_image_selected.label.image = tk_img  # Mantiene la referencia
        add_image_selected.label.place(x=400, y=50)

def add_image_solution(grafo, name, solution, close=True):
    dibujar_grafo(grafo[0], grafo[1], name, solution, close)
    img = Image.open(name)  # Abre la imagen con PIL
    img = img.resize((500, 500))  # Redimensiona la imagen si es necesario
    tk_img = ImageTk.PhotoImage(img)  # Convierte la imagen para Tkinter
    # Crea el widget de etiqueta o actualiza la imagen si ya existe
    if hasattr(add_image_solution, "label"):
        add_image_solution.label.configure(image=tk_img)
        add_image_solution.label.image = tk_img  # Mantiene la referencia
    else:
        add_image_solution.label = tk.Label(root, image=tk_img)
        add_image_solution.label.image = tk_img  # Mantiene la referencia
        add_image_solution.label.place(x=1000, y=50)


def usar_algoritmo_genetico(poblacion, generaciones, prob_mutacion):
    # Ejecución del programa con grafo dirigido o no dirigido
    print("\n---------------Grafo---------------")
    print(f"Grafo: {grafo_seleccionado[0]}")
    print(f"Dirigido: {grafo_seleccionado[1]}")
    print(f"Población: {poblacion}")
    print(f"Generaciones: {generaciones}")
    print(f"Probabilidad de mutación: {prob_mutacion}")
    print("---------------Resultados---------------")
    mejor_solucion_no_dirigido = algoritmo_genetico(grafo_seleccionado[0], poblacion, generaciones, prob_mutacion,dirigido=grafo_seleccionado[1])
    print("---------------Solución---------------")
    print("Mejor solución encontrada:", mejor_solucion_no_dirigido)
    add_image_solution(grafo_seleccionado, "files/solucion_grafo.png", mejor_solucion_no_dirigido, False)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Proyecto Grafos Geneticos")
    root.geometry("1566x568")
    root.resizable(False, False)
    root.config(bg="black")

    grafos = lector()

    add_title("Proyecto Algoritmos Genéticos")

    population_size = add_input("Tamaño de la población", 51, 50, 51, 100)
    generations = add_input("Generaciones", 51, 130, 51, 180)
    mutation_prob = add_input("Probabilidad de mutación", 51, 210, 51, 260)

    select = add_select_graph(
        "<<ListboxSelect>>",
        lambda event:
        add_image_selected(grafos[event.widget.curselection()[0]], "files/grafo.png"),
        51,
        320
    )

    button = add_button(
        "Ejecutar",
        "<Button-1>",
        lambda event: usar_algoritmo_genetico(
            int(population_size.get()),
            int(generations.get()),
            float(mutation_prob.get())
        ),
        51,
        480
    )

    root.mainloop()
