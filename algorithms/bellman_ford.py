import networkx as nx
import random
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
import pandas as pd


def bellman_ford_algorithm(graph, source):
    """
    Implémente l'algorithme de Bellman-Ford pour trouver les plus courts chemins dans un graphe.
    Gère les poids négatifs et détecte les cycles.
    """
    try:
        distances, paths = nx.single_source_bellman_ford(graph, source=source)
        return distances, paths
    except nx.NetworkXUnbounded:
        raise ValueError("Le graphe contient un cycle de poids négatif accessible depuis la source.")


def execute_bellman_ford():
    """
    Interface utilisateur pour exécuter l'algorithme de Bellman-Ford.
    """
    try:
        num_nodes = int(simpledialog.askstring("Entrée", "Entrez le nombre de sommets (nœuds) du graphe :"))
        num_edges = int(simpledialog.askstring("Entrée", "Entrez le nombre d'arêtes du graphe :"))
        if num_nodes <= 1 or num_edges < num_nodes - 1:
            raise ValueError("Le graphe doit avoir au moins 2 sommets et un nombre suffisant d'arêtes.")
    except (ValueError, TypeError):
        messagebox.showerror("Erreur", "Entrées invalides. Veuillez entrer des entiers valides.")
        return

    # Génération aléatoire d'un graphe orienté avec des poids
    graph = nx.DiGraph()
    graph.add_nodes_from(range(num_nodes))
    edges = set()
    while len(edges) < num_edges:
        u, v = random.sample(range(num_nodes), 2)
        weight = random.randint(-10, 20)  # Poids des arêtes pouvant être négatifs
        if u != v and (u, v) not in edges:
            edges.add((u, v))
            graph.add_edge(u, v, weight=weight)

    # Choisir un sommet source aléatoire
    source = random.choice(list(graph.nodes))

    try:
        # Exécution de l'algorithme de Bellman-Ford
        distances, paths = bellman_ford_algorithm(graph, source)

        # Affichage des résultats
        afficher_resultats(graph, distances, paths, source)
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))


def afficher_resultats(graph, distances, paths, source):
    """
    Affiche les résultats de l'algorithme de Bellman-Ford.
    """
    # Résultats textuels
    result_table = []
    for target, distance in distances.items():
        path_str = " -> ".join(map(str, paths[target]))
        result_table.append({"Destination": target, "Distance": distance, "Chemin": path_str})

    # Afficher les résultats dans une fenêtre Tkinter
    result_str = f"Distances minimales depuis le sommet source {source} :\n\n"
    result_str += "\n".join([f"Vers {row['Destination']} : Distance = {row['Distance']}, Chemin = {row['Chemin']}" 
                             for row in result_table])
    messagebox.showinfo("Résultats Bellman-Ford", result_str)

    # Présentation sous forme de tableau dans la console
    df = pd.DataFrame(result_table)
    print("\n### Résultats Bellman-Ford ###")
    print(df)

    # Visualisation du graphe
    pos = nx.spring_layout(graph, seed=42)  # Layout stable
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    node_colors = ["red" if node == source else "blue" for node in graph.nodes]
    shortest_path_edges = [(paths[target][i], paths[target][i + 1])
                           for target in paths for i in range(len(paths[target]) - 1)]

    plt.figure(figsize=(12, 8))

    # Dessiner le graphe complet
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=700,
        font_weight="bold",
        font_color="white",
        edge_color="black",
        alpha=0.5
    )

    # Mettre en évidence les chemins optimaux
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=shortest_path_edges,
        edge_color="red",
        width=2
    )

    # Ajouter les poids des arêtes
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

    # Ajouter le titre et afficher
    plt.title(f"Graphe avec Bellman-Ford (Source : {source})")
    plt.tight_layout()
    plt.show()


# Exemple d'exécution
if __name__ == "__main__":
    execute_bellman_ford()
