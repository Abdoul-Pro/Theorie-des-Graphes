"""
Application graphique — Graphe de connaissances du quartier Tampouy
Universite Joseph Ki-Zerbo | Licence 1 Informatique | Groupe 5
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================
# DONNEES
# ==========================

NOEUDS = [
    ("Quartier Tampouy", "Quartier"),
    ("Maison 1", "Maison"),
    ("Maison 2", "Maison"),
    ("Fadal", "Adulte"),
    ("Djemila", "Adulte"),
    ("Khalilou", "Enfant"),
    ("Idrissa", "Adolescent"),
    ("Aboubacar", "Personne agee"),
    ("Ecole Primaire", "Ecole"),
    ("Boutique Gouemzy", "Commerce"),
    ("CSPS Tampouy", "Centre de sante"),
    ("Route Principale", "Route"),
]

RELATIONS = [
    ("Maison 1", "Quartier Tampouy", "EST_DANS"),
    ("Maison 2", "Quartier Tampouy", "EST_DANS"),
    ("Fadal", "Maison 1", "HABITE"),
    ("Djemila", "Maison 1", "HABITE"),
    ("Khalilou", "Maison 1", "HABITE"),
    ("Aboubacar", "Maison 2", "HABITE"),
    ("Idrissa", "Maison 2", "HABITE"),
    ("Khalilou", "Ecole Primaire", "FREQUENTE"),
    ("Idrissa", "Ecole Primaire", "FREQUENTE"),
    ("Fadal", "Boutique Gouemzy", "TRAVAILLE_DANS"),
    ("Aboubacar", "CSPS Tampouy", "SE_SOIGNE_A"),
    ("Boutique Gouemzy", "Route Principale", "EST_SITUE_SUR"),
    ("CSPS Tampouy", "Route Principale", "EST_SITUE_SUR"),
]

COULEURS = {
    "Quartier": "#FF8C00",
    "Maison": "#90EE90",
    "Adulte": "#87CEEB",
    "Enfant": "#87CEEB",
    "Adolescent": "#87CEEB",
    "Personne agee": "#87CEEB",
    "Ecole": "#FFD700",
    "Commerce": "#9370DB",
    "Centre de sante": "#FF6347",
    "Route": "#D3D3D3",
}

POSITIONS = {
    "Route Principale": (0, 6),
    "Quartier Tampouy": (0, 4),
    "Maison 1": (-2.5, 2),
    "Maison 2": (2.5, 2),
    "Fadal": (-3.5, 0),
    "Djemila": (-2.2, -1),
    "Khalilou": (-1, 0),
    "Aboubacar": (4, 0),
    "Idrissa": (1, 0),
    "Ecole Primaire": (0, -3),
    "Boutique Gouemzy": (-6, 2),
    "CSPS Tampouy": (6, 2),
}

# ==========================
# COULEURS UI
# ==========================

BG = "#1E1E2E"
BG_CARD = "#2A2A3C"
BG_HOVER = "#3A3A4C"
FG = "#E0E0E0"
FG_DIM = "#888899"
ACCENT = "#7C5CFC"
ACCENT_HOVER = "#9B7FFD"
GREEN = "#4ADE80"


# ==========================
# CREATION DU GRAPHE
# ==========================

def creer_graphe() -> nx.DiGraph:
    G = nx.DiGraph()
    for nom, type_noeud in NOEUDS:
        G.add_node(nom, type=type_noeud)
    for src, dst, relation in RELATIONS:
        G.add_edge(src, dst, relation=relation)
    return G


def couleur_noeud(G, noeud):
    return COULEURS.get(G.nodes[noeud].get("type", ""), "#FFFFFF")


# ==========================
# APPLICATION
# ==========================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graphe de connaissances — Quartier Tampouy")
        self.configure(bg=BG)
        self.minsize(900, 600)

        # Adapter a la taille de l'ecran
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"{int(w * 0.85)}x{int(h * 0.85)}+{int(w * 0.075)}+{int(h * 0.075)}")

        self.G = creer_graphe()

        self._build_ui()
        self.bind("<Configure>", self._on_resize)

    # ---- Construction de l'interface ----

    def _build_ui(self):
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # === HEADER ===
        header = tk.Frame(main, bg=BG)
        header.pack(fill="x", pady=(0, 10))

        self.titre = tk.Label(
            header,
            text="Graphe de connaissances",
            font=("Segoe UI", 22, "bold"),
            fg=FG, bg=BG,
        )
        self.titre.pack(anchor="w")

        self.soustitre = tk.Label(
            header,
            text="Modeles d'un quartier — Universite Joseph Ki-Zerbo | L1 Informatique | Groupe 5",
            font=("Segoe UI", 11),
            fg=FG_DIM, bg=BG,
        )
        self.soustitre.pack(anchor="w")

        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=(0, 10))

        # === CONTENU EN DEUX COLONNES ===
        self.body = tk.Frame(main, bg=BG)
        self.body.pack(fill="both", expand=True)

        # Colonne gauche
        self.left = tk.Frame(self.body, bg=BG)
        self.left.pack(side="left", fill="y", padx=(0, 15))

        self._build_carte_stats(self.left)
        self._build_carte_noeuds(self.left)
        self._build_carte_actions(self.left)

        # Colonne droite
        self.right = tk.Frame(self.body, bg=BG)
        self.right.pack(side="right", fill="both", expand=True)

        self._build_carte_graphe(self.right)

    # ---- Carte : Statistiques (Noeud uniquement) ----

    def _build_carte_stats(self, parent):
        self.card_stats = tk.Frame(parent, bg=BG_CARD, highlightbackground="#3A3A4C", highlightthickness=1)
        self.card_stats.pack(fill="x", pady=(0, 10))

        tk.Label(self.card_stats, text="STATISTIQUES", font=("Segoe UI", 10, "bold"),
                 fg=ACCENT, bg=BG_CARD).pack(anchor="w", padx=15, pady=(12, 8))

        row = tk.Frame(self.card_stats, bg=BG_CARD)
        row.pack(fill="x", padx=15, pady=(0, 10))
        tk.Label(row, text="Noeuds", font=("Segoe UI", 10), fg=FG_DIM, bg=BG_CARD).pack(side="left")
        tk.Label(row, text=str(self.G.number_of_nodes()), font=("Segoe UI", 10, "bold"),
                 fg=GREEN, bg=BG_CARD).pack(side="right")

    # ---- Carte : Noeuds ----

    def _build_carte_noeuds(self, parent):
        self.card_noeuds = tk.Frame(parent, bg=BG_CARD, highlightbackground="#3A3A4C", highlightthickness=1)
        self.card_noeuds.pack(fill="x", pady=(0, 10))

        tk.Label(self.card_noeuds, text="NOEUDS DU GRAPHE", font=("Segoe UI", 10, "bold"),
                 fg=ACCENT, bg=BG_CARD).pack(anchor="w", padx=15, pady=(12, 8))

        container = tk.Frame(self.card_noeuds, bg=BG_CARD)
        container.pack(fill="x", padx=15, pady=(0, 10))

        for nom, type_noeud in NOEUDS:
            row = tk.Frame(container, bg=BG_CARD)
            row.pack(fill="x", pady=1)

            couleur = COULEURS.get(type_noeud, "#FFFFFF")
            tk.Label(row, text="  ", bg=couleur, width=2).pack(side="left", padx=(0, 8))
            tk.Label(row, text=nom, font=("Segoe UI", 9), fg=FG, bg=BG_CARD, anchor="w").pack(side="left")
            tk.Label(row, text=type_noeud, font=("Segoe UI", 8), fg=FG_DIM, bg=BG_CARD, anchor="e").pack(side="right")

    # ---- Carte : Actions ----

    def _build_carte_actions(self, parent):
        self.card_actions = tk.Frame(parent, bg=BG_CARD, highlightbackground="#3A3A4C", highlightthickness=1)
        self.card_actions.pack(fill="x", pady=(0, 10))

        tk.Label(self.card_actions, text="ACTIONS", font=("Segoe UI", 10, "bold"),
                 fg=ACCENT, bg=BG_CARD).pack(anchor="w", padx=15, pady=(12, 8))

        btn_gen = tk.Button(
            self.card_actions,
            text="Generer et enregistrer l'image",
            font=("Segoe UI", 11, "bold"),
            fg="#FFFFFF", bg=ACCENT,
            activeforeground="#FFFFFF", activebackground=ACCENT_HOVER,
            relief="flat", cursor="hand2",
            command=self._generer_image,
        )
        btn_gen.pack(fill="x", padx=15, pady=(0, 12), ipady=8)

    # ---- Carte : Graphe ----

    def _build_carte_graphe(self, parent):
        self.card_graphe = tk.Frame(parent, bg=BG_CARD, highlightbackground="#3A3A4C", highlightthickness=1)
        self.card_graphe.pack(fill="both", expand=True)

        header_frame = tk.Frame(self.card_graphe, bg=BG_CARD)
        header_frame.pack(fill="x", padx=15, pady=(12, 0))

        tk.Label(header_frame, text="APERCU DU GRAPHE", font=("Segoe UI", 10, "bold"),
                 fg=ACCENT, bg=BG_CARD).pack(side="left")

        self.info_label = tk.Label(
            header_frame,
            text="L'aperçu du graphe peut varier selon la taille de l'écran. Pour un rendu optimal, cliquez sur « Générer et enregistrer l'image »",
            font=("Segoe UI", 8, "italic"), fg="#FF6B6B", bg=BG_CARD,
            anchor="w",
        )
        self.info_label.pack(side="left", padx=(15, 0), fill="x", expand=True)

        self.zone_graphe = tk.Frame(self.card_graphe, bg=BG_CARD)
        self.zone_graphe.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self._afficher_apercu_defaut()

    def _afficher_apercu_defaut(self):
        for w in self.zone_graphe.winfo_children():
            w.destroy()

        self.update_idletasks()
        largeur = max(self.zone_graphe.winfo_width(), 400)
        hauteur = max(self.zone_graphe.winfo_height(), 300)
        fig_w = largeur / 100
        fig_h = hauteur / 100

        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=100)
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        color_map = [couleur_noeud(self.G, n) for n in self.G.nodes()]

        nx.draw(
            self.G, POSITIONS, ax=ax,
            with_labels=True, node_color=color_map, node_size=3200,
            edgecolors="black", linewidths=2, font_size=10,
            font_weight="bold",
            arrows=True, arrowsize=20, edge_color="black",
        )
        edge_labels = nx.get_edge_attributes(self.G, "relation")
        nx.draw_networkx_edge_labels(
            self.G, POSITIONS, edge_labels=edge_labels,
            font_size=8, bbox=dict(facecolor="white", edgecolor="none", alpha=0.8),
            ax=ax,
        )
        ax.set_title("Graphe de connaissances du quartier Tampouy",
                      fontsize=16, fontweight="bold", pad=15)
        ax.axis("off")
        plt.tight_layout(pad=1)

        canvas = FigureCanvasTkAgg(fig, master=self.zone_graphe)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    # ---- Redimensionnement ----

    def _on_resize(self, event):
        if event.widget == self:
            self.after_cancel(self._resize_after) if hasattr(self, "_resize_after") else None
            self._resize_after = self.after(150, self._afficher_apercu_defaut)

    # ---- Actions ----

    def _generer_image(self):
        chemin = filedialog.asksaveasfilename(
            title="Enregistrer l'image du graphe",
            initialfile="graphe_tampouy.png",
            defaultextension=".png",
            filetypes=[("Image PNG", "*.png")],
            parent=self,
        )
        if not chemin:
            return

        fig, ax = plt.subplots(figsize=(15, 10), dpi=150)
        color_map = [couleur_noeud(self.G, n) for n in self.G.nodes()]

        nx.draw(
            self.G, POSITIONS, ax=ax,
            with_labels=True, node_color=color_map, node_size=3200,
            edgecolors="black", linewidths=2, font_size=10,
            font_weight="bold", arrows=True, arrowsize=20, edge_color="black",
        )
        edge_labels = nx.get_edge_attributes(self.G, "relation")
        nx.draw_networkx_edge_labels(
            self.G, POSITIONS, edge_labels=edge_labels, font_size=8,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.8), ax=ax,
        )
        ax.set_title("Graphe de connaissances du quartier Tampouy",
                      fontsize=16, fontweight="bold", pad=15)
        ax.axis("off")
        plt.tight_layout()
        plt.savefig(chemin, dpi=150, bbox_inches="tight")
        plt.close(fig)

        messagebox.showinfo("Succes", f"Image sauvegardee :\n{chemin}", parent=self)


# ==========================
# LANCEMENT
# ==========================

if __name__ == "__main__":
    app = App()
    app.mainloop()
