import networkx as nx
import random
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt


def kruskal_algorithm(graph):
    """
    Implémente l'algorithme de Kruskal pour trouver l'arbre couvrant minimal (MST).
    """
    # Trier les arêtes par poids croissant
    edges = sorted(graph.edges(data=True), key=lambda x: x[2]["weight"])
    mst = nx.Graph()
    mst.add_nodes_from(graph.nodes)

    subsets = {node: node for node in graph.nodes}

    def find(node):
        """
        Trouve le représentant d'un ensemble (utilisé pour détecter les cycles).
        """
        if subsets[node] != node:
            subsets[node] = find(subsets[node])
        return subsets[node]

    def union(node1, node2):
        """
        Réalise l'union de deux ensembles.
        """
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            subsets[root2] = root1

    mst_edges = []
    total_weight = 0

    # Ajout des arêtes au MST tout en évitant les cycles
    for u, v, data in edges:
        if find(u) != find(v):
            union(u, v)
            mst.add_edge(u, v, weight=data["weight"])
            mst_edges.append((u, v, data["weight"]))
            total_weight += data["weight"]

    return mst, mst_edges, total_weight, edges


def execute_kruskal():
    """
    Interface utilisateur pour exécuter l'algorithme de Kruskal.
    """
    try:
        num_nodes = int(simpledialog.askstring("Entrée", "Entrez le nombre de sommets du graphe :"))
        num_edges = int(simpledialog.askstring("Entrée", "Entrez le nombre d'arêtes du graphe :"))
    except (ValueError, TypeError):
        messagebox.showerror("Erreur", "Entrées invalides. Veuillez entrer des entiers valides.")
        return

    # Génération aléatoire du graphe
    graph = nx.Graph()
    graph.add_nodes_from(range(num_nodes))
    edges = set()
    while len(edges) < num_edges:
        u, v = random.sample(range(num_nodes), 2)
        weight = random.randint(1, 20)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            graph.add_edge(u, v, weight=weight)

    # Exécution de l'algorithme de Kruskal
    mst, mst_edges, total_weight, all_edges = kruskal_algorithm(graph)

    # Affichage des résultats
    result = f"Arbre couvrant minimal (Poids total : {total_weight}):\n"
    for u, v, weight in mst_edges:
        result += f"Arête ({u}, {v}) avec poids {weight}\n"
    messagebox.showinfo("Résultats Kruskal", result)

    # Visualisation du graphe
    afficher_graphe(graph, mst, all_edges, total_weight)


def afficher_graphe(graph, mst, all_edges, total_weight):
    """
    Affiche le graphe original et l'arbre couvrant minimal (MST) obtenu.
    """
    pos = nx.spring_layout(graph)

    # Coloration des arêtes
    edge_colors = [
        "green" if (u, v) in mst.edges or (v, u) in mst.edges else "red"
        for u, v, _ in all_edges
    ]

    plt.figure(figsize=(10, 8))
    # Graphe complet
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=700,
        font_weight="bold",
    )
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    # Dessiner les arêtes avec les couleurs appropriées
    nx.draw_networkx_edges(graph, pos, edgelist=all_edges, edge_color=edge_colors, width=2)

    # Arbre couvrant minimal
    nx.draw(
        mst,
        pos,
        with_labels=True,
        node_color="lightgreen",
        node_size=700,
        font_weight="bold",
    )
    nx.draw_networkx_edge_labels(mst, pos, edge_labels=nx.get_edge_attributes(mst, "weight"))

    plt.title(f"Arbre couvrant minimal (Poids total : {total_weight})")
    plt.show()
