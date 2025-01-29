import numpy as np
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt


def moindre_cout_method(supply, demand, cost_matrix):
    """
    Applique la méthode du Moindre Coût pour générer une solution initiale optimale.
    """
    rows, cols = len(supply), len(demand)
    allocation = np.zeros((rows, cols), dtype=int)
    total_cost = 0

    # Liste des coûts triés
    cost_indices = sorted(
        [(i, j) for i in range(rows) for j in range(cols)],
        key=lambda x: cost_matrix[x[0]][x[1]]
    )

    # Allocation des ressources en fonction des coûts les plus bas
    for i, j in cost_indices:
        if supply[i] > 0 and demand[j] > 0:
            qty = min(supply[i], demand[j])
            allocation[i, j] = qty
            supply[i] -= qty
            demand[j] -= qty
            total_cost += qty * cost_matrix[i, j]

    return allocation, total_cost


def execute_moindre_cout():
    """
    Interface utilisateur pour exécuter la méthode du Moindre Coût.
    """
    try:
        # Entrée utilisateur
        supply = simpledialog.askstring("Entrée", "Entrez les capacités des usines (séparées par des espaces) :")
        demand = simpledialog.askstring("Entrée", "Entrez les demandes des destinations (séparées par des espaces) :")
        cost_matrix_str = simpledialog.askstring(
            "Entrée", "Entrez la matrice des coûts (lignes séparées par des points-virgules, colonnes par des espaces) :"
        )

        # Conversion et validation des données
        supply = list(map(int, supply.split()))
        demand = list(map(int, demand.split()))
        cost_matrix = np.array([list(map(int, row.split())) for row in cost_matrix_str.split(";")])

        # Vérification que l'offre totale est égale à la demande totale
        if sum(supply) != sum(demand):
            messagebox.showerror("Erreur", "La somme des capacités doit être égale à la somme des demandes.")
            return

        # Exécution de la méthode du Moindre Coût
        allocation, total_cost = moindre_cout_method(supply.copy(), demand.copy(), cost_matrix)

        # Affichage des résultats
        afficher_resultats(allocation, cost_matrix, total_cost)

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")


def afficher_resultats(allocation, cost_matrix, total_cost):
    """
    Affiche les résultats sous forme de tableau graphique.
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

    # Affichage graphique
    ax.axis("tight")
    ax.axis("off")
    ax.table(cellText=table_data, loc="center", cellLoc="center")
    plt.title("Résultats de la méthode du Moindre Coût")
    plt.show()
