import networkx as nx
import random
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib import cm
from itertools import combinations


def welsh_powell_coloring(graph):
    """
    Implémente l'algorithme Welsh-Powell pour colorier un graphe.
    """
    sorted_nodes = sorted(graph.nodes, key=lambda x: graph.degree[x], reverse=True)
    colors = {}
    current_color = 0

    for node in sorted_nodes:
        if node not in colors:
            current_color += 1
            colors[node] = current_color
            for other_node in sorted_nodes:
                if other_node not in colors and all(
                    colors.get(neighbor) != current_color
                    for neighbor in graph.neighbors(other_node)
                ):
                    colors[other_node] = current_color
    return colors, current_color


def generate_dense_graph(num_nodes, density=0.5):
    """
    Génère un graphe dense en fonction du nombre de sommets et de la densité.
    La densité est une valeur entre 0 et 1 indiquant la proportion d'arêtes présentes.
    """
    graph = nx.Graph()
    graph.add_nodes_from(range(num_nodes))

    all_possible_edges = list(combinations(range(num_nodes), 2))
    num_edges = int(len(all_possible_edges) * density)
    sampled_edges = random.sample(all_possible_edges, num_edges)

    graph.add_edges_from(sampled_edges)
    return graph


def execute_welshpowell():
    """
    Exécute l'algorithme Welsh-Powell et affiche le graphe colorié.
    """
    try:
        num_nodes = int(simpledialog.askstring("Entrée", "Entrez le nombre de sommets du graphe (max 500) :"))
        if num_nodes < 1 or num_nodes > 500:
            raise ValueError("Le nombre de sommets doit être compris entre 1 et 500.")

        density = float(simpledialog.askstring("Entrée", "Entrez la densité des arêtes (0.1 à 1) :"))
        if density <= 0 or density > 1:
            raise ValueError("La densité doit être un nombre entre 0.1 et 1.")
    except (ValueError, TypeError):
        messagebox.showerror("Erreur", "Entrées invalides. Veuillez entrer des valeurs correctes.")
        return

    # Génération d'un graphe dense
    graph = generate_dense_graph(num_nodes, density)

    # Application de l'algorithme Welsh-Powell
    colors, chromatic_number = welsh_powell_coloring(graph)

    # Résultats
    result = f"Nombre chromatique (Chromatic Number) : {chromatic_number}\n\n"
    result += "\n".join([f"Sommets {node} -> Couleur {color}" for node, color in colors.items()])
    messagebox.showinfo("Résultats Welsh-Powell", result)

    # Affichage du graphe colorié
    pos = nx.spring_layout(graph)
    color_map = [colors[node] for node in graph.nodes]
    plt.figure(figsize=(12, 10))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=color_map,
        node_size=500,
        cmap=cm.get_cmap("rainbow", chromatic_number),
        font_color="white",
    )
    plt.title(f"Coloriage du graphe (Nombre chromatique : {chromatic_number})")
    plt.show()
