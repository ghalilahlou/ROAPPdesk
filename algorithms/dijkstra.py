import networkx as nx
import random
from tkinter import simpledialog, messagebox, Toplevel, Text, Scrollbar, END, VERTICAL
import matplotlib.pyplot as plt


def dijkstra_algorithm(graph, source):
    """
    Implémente l'algorithme de Dijkstra pour trouver les plus courts chemins à partir d'un sommet source.
    """
    distances, paths = nx.single_source_dijkstra(graph, source=source)
    return distances, paths


def execute_dijkstra():
    """
    Interface utilisateur pour exécuter l'algorithme de Dijkstra.
    """
    try:
        # Demande le nombre de sommets et d'arêtes
        num_nodes = int(simpledialog.askstring("Entrée", "Entrez le nombre de sommets du graphe (max 500) :"))
        if num_nodes < 1 or num_nodes > 500:
            raise ValueError("Le nombre de sommets doit être compris entre 1 et 500.")

        num_edges = int(simpledialog.askstring("Entrée", f"Entrez le nombre d'arêtes du graphe (max {num_nodes * (num_nodes - 1) // 2}) :"))
        if num_edges < 1 or num_edges > num_nodes * (num_nodes - 1) // 2:
            raise ValueError("Le nombre d'arêtes est invalide pour le nombre de sommets.")
    except (ValueError, TypeError):
        messagebox.showerror("Erreur", "Entrées invalides. Veuillez entrer des valeurs correctes.")
        return

    # Génération aléatoire du graphe
    graph = nx.Graph()
    graph.add_nodes_from(range(num_nodes))
    edges = set()
    while len(edges) < num_edges:
        u, v = random.sample(range(num_nodes), 2)
        weight = random.randint(1, 100)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            graph.add_edge(u, v, weight=weight)

    # Choisir un sommet source aléatoire
    source = random.choice(list(graph.nodes))

    # Exécution de l'algorithme de Dijkstra
    distances, paths = dijkstra_algorithm(graph, source)

    # Affichage des résultats
    afficher_resultats(graph, distances, paths, source)


def afficher_resultats(graph, distances, paths, source):
    """
    Affiche les résultats de l'algorithme de Dijkstra sous forme de tableau et dans un graphique.
    """
    # Fenêtre pour afficher les résultats
    result_window = Toplevel()
    result_window.title("Résultats de Dijkstra")
    result_window.geometry("600x400")

    # Zone de texte avec défilement pour les résultats
    text_widget = Text(result_window, wrap="none", font=("Courier", 10))
    scroll_y = Scrollbar(result_window, orient=VERTICAL, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scroll_y.set)
    text_widget.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    # Résultats sous forme de tableau
    header = f"{'Destination':<15}{'Distance':<15}{'Chemin':<50}\n"
    text_widget.insert(END, header)
    text_widget.insert(END, "-" * 80 + "\n")
    for target, distance in distances.items():
        path = " -> ".join(map(str, paths[target]))
        row = f"{target:<15}{distance:<15}{path:<50}\n"
        text_widget.insert(END, row)

    # Visualisation du graphe
    pos = nx.spring_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    node_colors = ["green" if node == source else "blue" for node in graph.nodes]

    plt.figure(figsize=(12, 10))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=700,
        font_weight="bold",
        font_color="white",
    )
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
    plt.title(f"Graphe avec Dijkstra (Source : {source})")
    plt.show()

