import numpy as np
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt


def nord_ouest_method(supply, demand, cost_matrix):
    """
    Applique la méthode du Nord-Ouest pour générer une solution initiale.
    """
    rows, cols = len(supply), len(demand)
    allocation = np.zeros((rows, cols), dtype=int)
    i, j = 0, 0

    while i < rows and j < cols:
        qty = min(supply[i], demand[j])
        allocation[i, j] = qty
        supply[i] -= qty
        demand[j] -= qty

        if supply[i] == 0:
            i += 1
        elif demand[j] == 0:
            j += 1

    total_cost = np.sum(allocation * cost_matrix)
    return allocation, total_cost


def execute_nord_ouest():
    """
    Interface utilisateur pour exécuter la méthode du Nord-Ouest.
    """
    try:
        # Demande des données à l'utilisateur
        supply = simpledialog.askstring("Entrée", "Entrez les capacités des usines (séparées par des espaces) :")
        demand = simpledialog.askstring("Entrée", "Entrez les demandes des destinations (séparées par des espaces) :")
        cost_matrix_str = simpledialog.askstring(
            "Entrée", "Entrez la matrice des coûts (lignes séparées par des points-virgules, colonnes par des espaces) :"
        )

        # Validation et conversion des entrées
        supply = list(map(int, supply.split()))
        demand = list(map(int, demand.split()))
        cost_matrix = np.array([list(map(int, row.split())) for row in cost_matrix_str.split(";")])

        # Vérification que l'offre totale correspond à la demande totale
        if sum(supply) != sum(demand):
            messagebox.showerror("Erreur", "La somme des capacités doit être égale à la somme des demandes.")
            return

        # Exécution de la méthode du Nord-Ouest
        allocation, total_cost = nord_ouest_method(supply.copy(), demand.copy(), cost_matrix)

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

    # Dessiner le tableau
    ax.axis("tight")
    ax.axis("off")
    ax.table(cellText=table_data, loc="center", cellLoc="center")
    plt.title("Résultats de la méthode du Nord-Ouest")
    plt.show()
