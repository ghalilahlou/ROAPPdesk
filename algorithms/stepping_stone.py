import numpy as np
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt


def stepping_stone_method(supply, demand, cost_matrix, initial_allocation):
    """
    Applique l'algorithme Stepping Stone pour optimiser le coût total d'une solution initiale.
    """
    rows, cols = len(supply), len(demand)
    allocation = initial_allocation.copy()
    total_cost = np.sum(allocation * cost_matrix)

    while True:
        # Étape 1 : Calcul des potentiels u et v
        u = [None] * rows
        v = [None] * cols
        u[0] = 0  # Fixer un potentiel initial

        while None in u or None in v:
            for i in range(rows):
                for j in range(cols):
                    if allocation[i, j] > 0:  # Si la cellule est allouée
                        if u[i] is not None and v[j] is None:
                            v[j] = cost_matrix[i, j] - u[i]
                        elif v[j] is not None and u[i] is None:
                            u[i] = cost_matrix[i, j] - v[j]

        # Étape 2 : Calcul des coûts d'amélioration
        improvement_costs = np.full((rows, cols), np.inf)
        for i in range(rows):
            for j in range(cols):
                if allocation[i, j] == 0:  # Cellule vide
                    # Calcul du coût d'amélioration via un cycle
                    cycle = find_cycle(allocation, (i, j))
                    if cycle:
                        improvement_costs[i, j] = calculate_cycle_cost(cycle, cost_matrix)

        # Étape 3 : Vérification des coûts d'amélioration
        min_cost = improvement_costs.min()
        if min_cost >= 0:  # Si aucun coût d'amélioration négatif, on termine
            break

        # Étape 4 : Mise à jour de la solution
        i, j = np.unravel_index(np.argmin(improvement_costs), improvement_costs.shape)
        cycle = find_cycle(allocation, (i, j))
        update_allocation(allocation, cycle)

        # Mise à jour du coût total
        total_cost = np.sum(allocation * cost_matrix)

    return allocation, total_cost


def find_cycle(allocation, start):
    """
    Trouve un cycle dans l'allocation actuelle en partant d'une cellule donnée.
    """
    rows, cols = allocation.shape
    visited = set()
    stack = [(start, [])]

    while stack:
        (x, y), path = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        new_path = path + [(x, y)]

        if len(new_path) > 3 and new_path[0] == (x, y):
            return new_path[:-1]  # Cycle trouvé

        # Ajouter les voisins (horizontaux et verticaux)
        for i in range(rows):
            if allocation[i, y] > 0 and (i, y) != (x, y):
                stack.append(((i, y), new_path))
        for j in range(cols):
            if allocation[x, j] > 0 and (x, j) != (x, y):
                stack.append(((x, j), new_path))

    return None  # Aucun cycle trouvé


def calculate_cycle_cost(cycle, cost_matrix):
    """
    Calcule le coût d'amélioration pour un cycle donné.
    """
    total = 0
    sign = 1  # Alternance entre + et -
    for i, j in cycle:
        total += sign * cost_matrix[i, j]
        sign *= -1
    return total


def update_allocation(allocation, cycle):
    """
    Met à jour l'allocation en fonction du cycle trouvé.
    """
    quantities = [allocation[i, j] for i, j in cycle if allocation[i, j] > 0]
    delta = min(quantities)
    sign = 1
    for i, j in cycle:
        allocation[i, j] += sign * delta
        sign *= -1


def execute_stepping_stone():
    """
    Interface utilisateur pour exécuter l'algorithme Stepping Stone.
    """
    try:
        supply = simpledialog.askstring("Entrée", "Entrez les capacités des usines (séparées par des espaces) :")
        demand = simpledialog.askstring("Entrée", "Entrez les demandes (séparées par des espaces) :")
        cost_matrix_str = simpledialog.askstring(
            "Entrée", "Entrez la matrice des coûts (lignes séparées par des points-virgules, colonnes par des espaces) :"
        )

        supply = list(map(int, supply.split()))
        demand = list(map(int, demand.split()))
        cost_matrix = np.array([list(map(int, row.split())) for row in cost_matrix_str.split(";")])

        if sum(supply) != sum(demand):
            messagebox.showerror("Erreur", "La somme des capacités doit être égale à la somme des demandes.")
            return

        # Solution initiale via Moindre Coût
        initial_allocation, _, _ = moindre_cout_method(supply.copy(), demand.copy(), cost_matrix)

        # Appliquer l'algorithme Stepping Stone
        allocation, total_cost = stepping_stone_method(supply, demand, cost_matrix, initial_allocation)

        # Afficher les résultats
        afficher_resultats(allocation, cost_matrix, allocation * cost_matrix, total_cost)

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")


def moindre_cout_method(supply, demand, cost_matrix):
    """
    Génère une solution initiale en utilisant la méthode du moindre coût.
    """
    rows, cols = len(supply), len(demand)
    allocation = np.zeros((rows, cols), dtype=int)
    total_cost = 0

    cost_indices = sorted(
        [(i, j) for i in range(rows) for j in range(cols)],
        key=lambda x: cost_matrix[x[0]][x[1]],
    )

    for i, j in cost_indices:
        if supply[i] > 0 and demand[j] > 0:
            qty = min(supply[i], demand[j])
            allocation[i, j] = qty
            supply[i] -= qty
            demand[j] -= qty
            total_cost += qty * cost_matrix[i, j]

    return allocation, cost_matrix * allocation, total_cost


def afficher_resultats(allocation, cost_matrix, cost_details, total_cost):
    """
    Affiche les résultats dans un tableau graphique.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    rows, cols = allocation.shape
    table_data = [["" for _ in range(cols + 1)] for _ in range(rows + 2)]
    table_data[0][0] = "Coût"

    for j in range(cols):
        table_data[0][j + 1] = f"D{j + 1}"

    for i in range(rows):
        table_data[i + 1][0] = f"U{i + 1}"
        for j in range(cols):
            table_data[i + 1][j + 1] = f"{allocation[i, j]} ({cost_matrix[i, j]})"

    table_data[-1][0] = "Total"
    table_data[-1][1] = f"Coût Total = {total_cost}"

    ax.axis("tight")
    ax.axis("off")
    ax.table(cellText=table_data, loc="center", cellLoc="center")
    plt.title("Résultats de l'algorithme Stepping Stone")
    plt.show()
