import networkx as nx
import random
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Forcer Matplotlib à utiliser TkAgg comme backend
plt.switch_backend("TkAgg")


def potentiel_metra_algorithm_with_details(nodes, edges):
    """
    Applique l'algorithme de Potentiel Métra pour ordonnancer des tâches,
    calculer marges, chemin critique et durée totale.
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_weighted_edges_from(edges)

    # Initialisation des temps de début et de fin
    start_times = {node: 0 for node in nodes}
    finish_times = {node: 0 for node in nodes}
    levels = {node: 0 for node in nodes}

    try:
        sorted_nodes = list(nx.topological_sort(graph))
    except nx.NetworkXUnfeasible:
        raise ValueError("Le graphe contient un cycle. Assurez-vous que les dépendances sont valides.")

    # Calcul des temps de début et de fin
    for node in sorted_nodes:
        for predecessor in graph.predecessors(node):
            start_times[node] = max(start_times[node], finish_times[predecessor])
        finish_times[node] = start_times[node] + max(
            (graph[predecessor][node]['weight'] for predecessor in graph.predecessors(node)),
            default=0
        )
        levels[node] = (
            max(levels.get(predecessor, 0) + 1 for predecessor in graph.predecessors(node))
            if list(graph.predecessors(node)) else 0
        )

    total_duration = max(finish_times.values())  # Durée totale du projet

    # Calcul des marges (temps au plus tard)
    late_start = {node: total_duration for node in nodes}
    late_finish = {node: total_duration for node in nodes}

    for node in reversed(sorted_nodes):
        for successor in graph.successors(node):
            late_start[node] = min(late_start[node], late_finish[successor] - graph[node][successor]['weight'])
        late_finish[node] = late_start[node]

    # Calcul des marges libres et totales
    free_margin = {}
    for node in nodes:
        if list(graph.successors(node)):  # Vérifie si le nœud a des successeurs
            free_margin[node] = min(
                (late_start[succ] - finish_times[node]) for succ in graph.successors(node)
            )
        else:
            free_margin[node] = 0  # Pas de successeurs, marge libre = 0

    total_margin = {node: late_start[node] - start_times[node] for node in nodes}

    # Déterminer le chemin critique
    critical_path = [node for node in nodes if total_margin[node] == 0]

    # Assigner les niveaux comme un attribut aux nœuds
    nx.set_node_attributes(graph, levels, name="level")

    return {
        "start_times": start_times,
        "finish_times": finish_times,
        "late_start": late_start,
        "late_finish": late_finish,
        "free_margin": free_margin,
        "total_margin": total_margin,
        "critical_path": critical_path,
        "total_duration": total_duration,
        "graph": graph,
        "levels": levels,
    }


def generate_random_graph(num_nodes):
    """
    Génère un graphe orienté aléatoire représentant des tâches avec des dépendances.
    """
    nodes = list(range(1, num_nodes + 1))
    edges = set()

    for node in nodes[1:]:
        predecessors = random.sample(nodes[:node - 1], k=random.randint(1, min(3, node - 1)))
        for pred in predecessors:
            weight = random.randint(1, 10)
            edges.add((pred, node, weight))

    return nodes, list(edges)


def show_graph(graph, levels, critical_path):
    """
    Affiche le graphe de tâches avec leurs niveaux sous forme de diagramme.
    """
    # Vérification que tous les nœuds ont un niveau attribué
    for node in graph.nodes:
        if "level" not in graph.nodes[node]:
            raise ValueError(f"Le nœud {node} n'a pas d'attribut 'level'.")

    pos = nx.multipartite_layout(graph, subset_key="level")  # Utiliser 'level' comme clé pour les niveaux
    plt.figure(figsize=(12, 8))
    color_map = ["red" if node in critical_path else "lightblue" for node in graph.nodes]

    nx.draw(
        graph, pos, with_labels=True, node_size=700,
        node_color=color_map, font_size=10, font_weight="bold"
    )
    edge_labels = {(u, v): d["weight"] for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
    plt.title("Diagramme de Potentiel Métra (Chemin Critique en Rouge)", fontsize=14)
    plt.show()


def execute_potentiel_metra():
    """
    Interface utilisateur pour exécuter l'algorithme de Potentiel Métra.
    """
    try:
        num_nodes = int(simpledialog.askstring("Entrée", "Entrez le nombre de tâches (sommets) :"))
        if num_nodes <= 1:
            raise ValueError("Le nombre de tâches doit être supérieur à 1.")
    except (ValueError, TypeError):
        messagebox.showerror("Erreur", "Entrée invalide. Veuillez entrer un entier valide.")
        return

    nodes, edges = generate_random_graph(num_nodes)

    try:
        result = potentiel_metra_algorithm_with_details(nodes, edges)
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
        return

    # Afficher les résultats dans une nouvelle fenêtre
    display_results_in_window(result)


def display_results_in_window(result):
    """
    Affiche les résultats de l'algorithme dans une fenêtre Tkinter.
    """
    result_window = tk.Toplevel()
    result_window.title("Résultats Potentiel Métra")
    result_window.geometry("900x700")

    text_widget = ScrolledText(result_window, wrap=tk.WORD, font=("Arial", 10))
    text_widget.pack(fill=tk.BOTH, expand=True)

    # Résumé des résultats
    text_widget.insert(tk.END, "=== Résultats Potentiel Métra ===\n\n")
    text_widget.insert(tk.END, f"Durée totale du projet : {result['total_duration']} unités\n\n")
    text_widget.insert(tk.END, "Chemin Critique : " + " -> ".join(map(str, result['critical_path'])) + "\n\n")

    text_widget.insert(tk.END, "Temps de début et de fin :\n")
    for node in result['start_times']:
        text_widget.insert(
            tk.END,
            f"Tâche {node}: Début -> {result['start_times'][node]}, Fin -> {result['finish_times'][node]}\n"
        )

    text_widget.insert(tk.END, "\nTemps au plus tard :\n")
    for node in result['late_start']:
        text_widget.insert(
            tk.END,
            f"Tâche {node}: Début au plus tard -> {result['late_start'][node]}, "
            f"Fin au plus tard -> {result['late_finish'][node]}\n"
        )

    text_widget.insert(tk.END, "\nMarges :\n")
    for node in result['free_margin']:
        text_widget.insert(
            tk.END,
            f"Tâche {node}: Marge Libre -> {result['free_margin'][node]}, "
            f"Marge Totale -> {result['total_margin'][node]}\n"
        )

    # Bouton pour afficher le graphe
    tk.Button(
        result_window,
        text="Afficher le graphe",
        command=lambda: show_graph(result['graph'], result['levels'], result['critical_path']),
        font=("Helvetica", 12),
        bg="#4a90e2",
        fg="white",
        activebackground="#357ab7",
        width=25,
        height=2,
    ).pack(pady=20)

    # Bouton pour fermer la fenêtre
    tk.Button(
        result_window,
        text="Fermer",
        command=result_window.destroy,
        font=("Helvetica", 12),
        bg="#e74c3c",
        fg="white",
        activebackground="#c0392b",
        width=25,
        height=2,
    ).pack(pady=10)
