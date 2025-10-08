import tkinter as tk
from tkinter import ttk
from db_utils import get_decoupe_by_name

class LoadedDecoupe:
    def __init__(self, master, user_id, decoupe_name):
        self.master = master
        self.user_id = user_id
        self.decoupe_name = decoupe_name

        master.title("Visualisation de découpe")
        master.geometry("1250x720")
        master.resizable(False, False)
        master.configure(bg="#121212")  # fond sombre

        # Card central
        card = tk.Frame(master, bg="#f8fafc")
        card.place(relx=0.5, rely=0.5, anchor="center", width=1180, height=660)

        # Header
        header = tk.Frame(card, bg="#526787", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Visualisation de découpe", bg="#526787", fg="white",
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=20)
        tk.Label(header, text=f"Nom: {self.decoupe_name}    |    Utilisateur #{self.user_id}",
                 bg="#526787", fg="#e6eef8", font=("Segoe UI", 11)).pack(side="left", padx=12, pady=26)

        # Top info row
        info_row = tk.Frame(card, bg="#f8fafc")
        info_row.pack(fill="x", padx=18, pady=(12, 6))

        tk.Label(info_row, text="Découpe :", bg="#f8fafc", fg="#222", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(info_row, text=self.decoupe_name, bg="#f8fafc", fg="#444", font=("Segoe UI", 12)).grid(row=0, column=1, sticky="w", padx=(6,20))

        # Boutons d'action
        btns = tk.Frame(info_row, bg="#f8fafc")
        btns.grid(row=0, column=4, sticky="e")
        tk.Button(btns, text="Retour", bg="#6b7280", fg="white", bd=0, padx=10, pady=6, command=self.return_to_last_menu).pack(side="left", padx=6)

        # Tableau (Treeview) avec scrollbars
        table_frame = tk.Frame(card, bg="#f8fafc")
        table_frame.pack(fill="both", expand=True, padx=18, pady=(6,12))

        cols = ("reseau", "masque", "nb", "premiere", "derniere", "broadcast")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=18)
        headings = {
            "reseau": "Réseau",
            "masque": "Masque",
            "nb": "Nombre d'adresses",
            "premiere": "Première IP",
            "derniere": "Dernière IP",
            "broadcast": "Broadcast"
        }
        for c in cols:
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, anchor="center", width=180, stretch=True)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Alternance de couleurs pour lisibilité
        self.tree.tag_configure('oddrow', background='#ffffff')
        self.tree.tag_configure('evenrow', background='#f1f5f9')
        self.tree.tag_configure('header', background='#526787', foreground='white')

        # Footer (statut)
        footer = tk.Frame(card, bg="#f8fafc")
        footer.pack(fill="x", padx=18, pady=(0,12))
        self.status_lbl = tk.Label(footer, text="Prêt", bg="#f8fafc", fg="#666", font=("Segoe UI", 10))
        self.status_lbl.pack(side="left")

        # Charger les données initiales
        self.load_from_db()

    def load_from_db(self):
        loaded_decoupe = get_decoupe_by_name(self.decoupe_name)

        # Remplir le tableau
        for i, details in loaded_decoupe.items():
            self.tree.insert("", "end", values=(
                details["Réseau"],
                details["Masque"],
                details["Nombre total d'adresses"],
                details["Première IP utilisable"],
                details["Dernière IP utilisable"],
                details["Adresse de broadcast"]
            ))
    def return_to_last_menu(self):
        from select_decoupe import DecoupeSelector

        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        DecoupeSelector(new_window,self.user_id)