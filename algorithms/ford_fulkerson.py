import networkx as nx
import random
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt


def ford_fulkerson_algorithm(graph, source, sink):
    """
    Implémente l'algorithme de Ford-Fulkerson pour trouver le flux maximal dans un graphe.
    """
    residual_graph = graph.copy()
    for u, v, data in residual_graph.edges(data=True):
        data['flow'] = 0  # Initialiser le flux à 0

    max_flow = 0
    paths_taken = []  # Liste pour stocker les chemins augmentants

    def bfs_find_path():
        """
        Recherche d'un chemin augmentant en utilisant une recherche en largeur (BFS).
        """
        visited = {node: False for node in residual_graph.nodes}
        parent = {}
        queue = [source]
        visited[source] = True

        while queue:
            current = queue.pop(0)
            for neighbor in residual_graph.neighbors(current):
                capacity = residual_graph[current][neighbor]['capacity']
                flow = residual_graph[current][neighbor]['flow']
                if not visited[neighbor] and capacity > flow:  # Si un chemin valide est trouvé
                    parent[neighbor] = current
                    visited[neighbor] = True
                    queue.append(neighbor)
                    if neighbor == sink:
                        path = []
                        while neighbor in parent:
                            path.append((parent[neighbor], neighbor))
                            neighbor = parent[neighbor]
                        return path[::-1]  # Retourner le chemin dans le bon ordre
        return None

    while True:
        path = bfs_find_path()
        if not path:
            break

        # Trouver le goulot d'étranglement (capacité résiduelle minimale sur le chemin)
        path_flow = min(
            residual_graph[u][v]['capacity'] - residual_graph[u][v]['flow'] for u, v in path
        )

        # Mettre à jour les flux dans le graphe résiduel
        for u, v in path:
            residual_graph[u][v]['flow'] += path_flow
            if residual_graph.has_edge(v, u):
                residual_graph[v][u]['flow'] -= path_flow
            else:
                residual_graph.add_edge(v, u, capacity=0, flow=-path_flow)

        max_flow += path_flow
        paths_taken.append((path, path_flow))  # Ajouter le chemin et son flux au suivi

    return max_flow, residual_graph, paths_taken


def execute_ford_fulkerson():
    """
    Interface utilisateur pour exécuter l'algorithme de Ford-Fulkerson.
    """
    try:
        num_nodes = int(simpledialog.askstring("Entrée", "Entrez le nombre de sommets du graphe :"))
        num_edges = int(simpledialog.askstring("Entrée", "Entrez le nombre d'arêtes du graphe :"))
    except (ValueError, TypeError):
        messagebox.showerror("Erreur", "Entrées invalides. Veuillez entrer des entiers valides.")
        return

    # Générer un graphe orienté aléatoire
    graph = nx.DiGraph()
    graph.add_nodes_from(range(num_nodes))
    edges = set()
    while len(edges) < num_edges:
        u, v = random.sample(range(num_nodes), 2)
        if u != v:
            capacity = random.randint(5, 20)
            edges.add((u, v))
            graph.add_edge(u, v, capacity=capacity)

    source = 0
    sink = num_nodes - 1

    # Exécution de l'algorithme de Ford-Fulkerson
    max_flow, residual_graph, paths_taken = ford_fulkerson_algorithm(graph, source, sink)

    # Affichage des résultats
    afficher_resultats(graph, residual_graph, max_flow, source, sink, paths_taken)


def afficher_resultats(graph, residual_graph, max_flow, source, sink, paths_taken):
    """
    Affiche les résultats de l'algorithme Ford-Fulkerson avec le chemin optimal et les flux.
    """
    result = f"Flux maximal du sommet {source} au sommet {sink} : {max_flow}\n\n"
    result += "Détails des flux sur chaque arête :\n"
    for u, v, data in residual_graph.edges(data=True):
        result += f"Arête ({u} -> {v}): Flux = {data.get('flow', 0)}/{data['capacity']}\n"

    result += "\nChemins augmentants utilisés :\n"
    for i, (path, path_flow) in enumerate(paths_taken, start=1):
        path_str = " -> ".join(f"{u}->{v}" for u, v in path)
        result += f"Chemin {i} : {path_str} avec flux = {path_flow}\n"

    messagebox.showinfo("Résultats Ford-Fulkerson", result)

    # Visualisation des graphes
    pos = nx.spring_layout(graph)
    edge_labels = {
        (u, v): f"{data.get('flow', 0)}/{data['capacity']}" for u, v, data in residual_graph.edges(data=True)
    }

    # Premier graphe : Graphe principal avec flux
    plt.figure(figsize=(14, 10))
    plt.subplot(2, 1, 1)
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=700,
        font_weight="bold",
    )
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="red")
    plt.title(f"Graphe Résiduel - Flux Maximal: {max_flow}")

    # Deuxième graphe : Graphe avec chemin optimal
    plt.subplot(2, 1, 2)
    path_edges = [edge for path, _ in paths_taken for edge in path]
    edge_colors = ["red" if edge in path_edges else "black" for edge in residual_graph.edges]
    nx.draw(
        residual_graph,
        pos,
        with_labels=True,
        node_color="lightgreen",
        node_size=700,
        edge_color=edge_colors,
        edge_cmap=plt.cm.Reds,
        font_weight="bold",
    )
    nx.draw_networkx_edge_labels(residual_graph, pos, edge_labels=edge_labels, font_color="red")
    plt.title("Chemins augmentants (en rouge)")
    plt.tight_layout()
    plt.show()
