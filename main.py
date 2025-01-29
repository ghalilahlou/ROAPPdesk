import tkinter as tk
import sys
import os
import os
import sys
from PIL import Image, ImageTk, ImageDraw, ImageFont  # Assurez-vous d'avoir Pillow installé : pip install pillow
from tkinter import messagebox
from algorithms.welsh_powell import execute_welshpowell
from algorithms.dijkstra import execute_dijkstra
from algorithms.kruskal import execute_kruskal
from algorithms.bellman_ford import execute_bellman_ford
from algorithms.potentiel_metra import execute_potentiel_metra
from algorithms.moindre_cout import execute_moindre_cout
from algorithms.nord_ouest import execute_nord_ouest
from algorithms.stepping_stone import execute_stepping_stone
from algorithms.ford_fulkerson import execute_ford_fulkerson


def execute_algorithm(command, name):
    """
    Exécute un algorithme et gère les erreurs éventuelles.
    """
    try:
        command()
    except Exception as e:
        messagebox.showerror(
            "Erreur",
            f"Une erreur est survenue avec l'algorithme {name} :\n{str(e)}"
        )


def open_algo_menu():
    """
    Ouvre le menu des algorithmes avec des animations et un design amélioré.
    """
    algo_window = tk.Toplevel(gui)
    algo_window.title("Menu des Algorithmes")
    algo_window.geometry("800x600")
    algo_window.configure(bg="#282c34")  # Fond sombre et moderne

    # Titre du menu
    menu_label = tk.Label(
        algo_window,
        text="Choisissez un Algorithme",
        font=("Helvetica", 24, "bold"),
        fg="#61afef",  # Bleu moderne
        bg="#282c34",
    )
    menu_label.pack(pady=20)

    # Liste des algorithmes avec leur commande
    algo_list = [
        ("Welsh-Powell", execute_welshpowell),
        ("Dijkstra", execute_dijkstra),
        ("Kruskal", execute_kruskal),
        ("Bellman-Ford", execute_bellman_ford),
        ("Potentiel Métra", execute_potentiel_metra),
        ("Moindre Coût", execute_moindre_cout),
        ("Nord-Ouest", execute_nord_ouest),
        ("Stepping Stone", execute_stepping_stone),
        ("Ford-Fulkerson", execute_ford_fulkerson),
    ]

    # Création des boutons pour chaque algorithme
    button_frame = tk.Frame(algo_window, bg="#282c34")
    button_frame.pack(pady=20)

    for name, command in algo_list:
        tk.Button(
            button_frame,
            text=name,
            command=lambda cmd=command, n=name: execute_algorithm(cmd, n),
            font=("Helvetica", 14),
            bg="#98c379",  # Vert moderne
            fg="white",
            activebackground="#56b6c2",  # Bleu clair au survol
            activeforeground="white",
            width=30,
            height=2,
            bd=0,
            relief="raised",
        ).pack(pady=10)

    # Bouton pour revenir au menu principal
    exit_button = tk.Button(
        algo_window,
        text="Retour",
        command=algo_window.destroy,
        font=("Helvetica", 14, "bold"),
        bg="#e06c75",  # Rouge moderne
        fg="white",
        activebackground="#c74e53",  # Rouge clair au survol
        activeforeground="white",
        width=25,
        height=2,
        bd=0,
        relief="raised",
    )
    exit_button.pack(side="bottom", pady=20)


def open_main_window():
    """
    Ouvre la fenêtre principale avec un logo et une interface modernisée.
    """
    global gui
    gui = tk.Tk()
    gui.title("Graphes et Algorithmes")
    gui.geometry("800x600")
    gui.configure(bg="#1e2227")  # Fond sombre

    # Ajouter le logo
    try:
        logo_img = Image.open("/Users/ghali/ro /ROAPPdesk/logo-1.png")  # Utilisez le chemin complet
        logo_img = logo_img.resize((200, 200), Image.Resampling.LANCZOS)  # Redimensionner
        logo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(gui, image=logo, bg="#1e2227")
        logo_label.image = logo  # Garde une référence pour éviter le garbage collection
        logo_label.pack(pady=20)
    except Exception as e:
        messagebox.showwarning("Attention", f"Le logo n'a pas pu être chargé : {e}")

    # Titre principal
    title_label = tk.Label(
        gui,
        text="Bienvenue dans Graphes et Algorithmes",
        font=("Helvetica", 24, "bold"),
        fg="#61afef",  # Bleu moderne
        bg="#1e2227",  # Fond sombre
    )
    title_label.pack(pady=10)

    # Texte pour les crédits
    credits_frame = tk.Frame(gui, bg="#1e2227")
    credits_frame.pack(pady=10)

    # Ligne des noms
    names_label = tk.Label(
        credits_frame,
        text="By Ghali Lahlou, Yahia Benmansour",
        font=("Helvetica", 16, "italic"),
        fg="#98c379",  # Vert moderne
        bg="#1e2227",
    )
    names_label.pack(pady=2)

    # Ligne pour l'encadrant
    supervisor_label = tk.Label(
        credits_frame,
        text="Encadrant: Dr. El Mkhalet Mouna",
        font=("Helvetica", 16, "italic"),
        fg="#c678dd",  # Violet moderne
        bg="#1e2227",
    )
    supervisor_label.pack(pady=2)

    # Bouton pour ouvrir le menu des algorithmes
    open_button = tk.Button(
        gui,
        text="Ouvrir le Menu des Algorithmes",
        command=open_algo_menu,
        font=("Helvetica", 16),
        bg="#98c379",  # Vert moderne
        fg="white",
        activebackground="#56b6c2",  # Bleu clair au survol
        activeforeground="white",
        width=30,
        height=2,
        bd=0,
        relief="raised",
    )
    open_button.pack(pady=20)

    # Bouton pour quitter
    exit_button = tk.Button(
        gui,
        text="Quitter",
        command=gui.quit,
        font=("Helvetica", 16),
        bg="#e74c3c",  # Rouge doux
        fg="white",
        activebackground="#c0392b",  # Rouge foncé au survol
        activeforeground="white",
        width=30,
        height=2,
        bd=0,
        relief="raised",
    )
    exit_button.pack(pady=20)

    # Lancer l'application
    gui.mainloop()


if __name__ == "__main__":
    open_main_window()