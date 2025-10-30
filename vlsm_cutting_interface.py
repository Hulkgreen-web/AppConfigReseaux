import tkinter as tk
from tkinter import ttk, messagebox
from vlsm_subnet import VLSMSimple

class VlsmCuttingInterface:
    def __init__(self, master, ip_address, masque, nb_sr, nb_ip_needed, user_id=0):
        self.master = master
        self.ip_address = ip_address
        self.masque = masque
        self.nb_sr = nb_sr
        self.nb_ip_needed = nb_ip_needed
        self.user_id = user_id

        master.title("Calculateur de Sous-Réseaux")
        master.geometry("1250x720")
        master.minsize(900, 600)
        master.configure(bg="#121212")

        card = tk.Frame(master, bg="#f8fafc")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.94, relheight=0.92)

        header = tk.Frame(card, bg="#5a3bd6", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Calculateur de Sous-Réseaux", bg="#5a3bd6", fg="white",
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=18)
        tk.Label(header, text="Génère les sous-réseaux et leurs plages IP", bg="#5a3bd6",
                 fg="#e7e7ff", font=("Segoe UI", 10)).pack(side="left", padx=12, pady=28)

        input_frame = tk.Frame(card, bg="#f8fafc")
        input_frame.pack(fill="x", padx=18, pady=(14, 8))

        # configure columns for proportional spacing
        for i in range(8):
            input_frame.grid_columnconfigure(i, weight=1)

        tk.Label(input_frame, text="Adresse IP:", bg="#f8fafc", fg="#222", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w")
        self.ip_entry = tk.Entry(input_frame, font=("Segoe UI", 12), justify="center")
        self.ip_entry.grid(row=0, column=1, sticky="we", padx=4)
        self.ip_entry.insert(0, self.ip_address)
        self.ip_entry.config(state="readonly")

        tk.Label(input_frame, text="Masque CIDR:", bg="#f8fafc", fg="#222", font=("Segoe UI", 12)).grid(row=0, column=2, sticky="w")
        self.masque_entry = tk.Entry(input_frame, font=("Segoe UI", 12), justify="center")
        self.masque_entry.grid(row=0, column=3, sticky="we", padx=4)
        self.masque_entry.insert(0, str(self.masque).lstrip('/'))
        self.masque_entry.config(state="readonly")

        tk.Label(input_frame, text="Nombre de sous-réseaux:", bg="#f8fafc", fg="#222", font=("Segoe UI", 12)).grid(row=0, column=4, sticky="w")
        self.nb_sr_entry = tk.Entry(input_frame, font=("Segoe UI", 12), justify="center")
        self.nb_sr_entry.grid(row=0, column=5, sticky="we", padx=4)
        self.nb_sr_entry.insert(0, str(self.nb_sr))
        self.nb_sr_entry.config(state="readonly")

        tk.Label(input_frame, text="IPs par sous-réseau (séparés par , ; ou espace):", bg="#f8fafc", fg="#222", font=("Segoe UI", 12)).grid(row=1, column=0, columnspan=4, sticky="w", pady=(8,0))
        self.sr_entry = tk.Entry(input_frame, font=("Segoe UI", 12))
        self.sr_entry.grid(row=1, column=3, columnspan=3, sticky="we", padx=4, pady=(8,0))
        self.sr_entry.insert(0, self.nb_ip_needed)
        self.sr_entry.config(state="readonly")

        calc_btn = tk.Button(input_frame, text="Calculer", bg="#2b6cb0", fg="white", font=("Segoe UI", 12),
                             activebackground="#235a91", padx=12, command=self.calculer_sous_reseaux)
        calc_btn.grid(row=0, column=7, rowspan=2, sticky="nsew", padx=(10,0), pady=0)

        table_frame = tk.Frame(card, bg="#f8fafc")
        table_frame.pack(fill="both", expand=True, padx=18, pady=(6, 12))

        cols = ("reseau", "masque", "cidr", "nb", "premiere", "derniere", "broadcast")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        headings = {
            "reseau": "Réseau",
            "masque": "Masque",
            "cidr": "CIDR",
            "nb": "Nombre d'adresses",
            "premiere": "Première IP",
            "derniere": "Dernière IP",
            "broadcast": "Broadcast"
        }
        col_widths = [180, 110, 70, 140, 140, 140, 140]
        for c, w in zip(cols, col_widths):
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, anchor="center", width=w, stretch=True)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        footer = tk.Frame(card, bg="#f8fafc")
        footer.pack(fill="x", padx=18, pady=(0,12))

        info_lbl = tk.Label(footer, text=f"Utilisateur #{self.user_id}", bg="#f8fafc", fg="#666", font=("Segoe UI", 10))
        info_lbl.pack(side="left")

        menu_btn = tk.Button(footer, text="Retour au menu principal", bg="#6b7280", fg="white", font=("Segoe UI", 11),
                             activebackground="#4b5563", padx=12, command=self.open_main_menu)
        menu_btn.pack(side="right")

        self.tree.tag_configure('oddrow', background='#ffffff')
        self.tree.tag_configure('evenrow', background='#f1f5f9')

    def open_main_menu(self):
        from menu_principal import MenuPrincipal
        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        MenuPrincipal(new_window, self.user_id)

    def calculer_sous_reseaux(self):
        ip_depart = self.ip_entry.get().strip()
        masque_raw = self.masque_entry.get().strip()
        nb_sr_raw = self.nb_sr_entry.get().strip()
        liste_raw = self.sr_entry.get().strip()

        try:
            masque_cidr = int(masque_raw.lstrip('/').strip())
            if not (0 <= masque_cidr <= 32):
                raise ValueError
        except Exception:
            messagebox.showerror("Erreur", "Masque CIDR invalide. Exemple valide: 24")
            return

        try:
            nb_sr = int(nb_sr_raw)
            if nb_sr <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Erreur", "Nombre de sous-réseaux invalide.")
            return

        if not liste_raw:
            messagebox.showerror("Erreur", "Liste d'IPs requises vide.")
            return

        if ',' in liste_raw:
            parts = [p.strip() for p in liste_raw.split(',')]
        elif ';' in liste_raw:
            parts = [p.strip() for p in liste_raw.split(';')]
        else:
            parts = [p.strip() for p in liste_raw.split()]

        try:
            required = [int(p) for p in parts if p != '']
        except ValueError:
            messagebox.showerror("Erreur", "La liste doit contenir uniquement des entiers.")
            return

        if len(required) != nb_sr:
            messagebox.showerror("Erreur", f"Vous avez indiqué {nb_sr} sous-réseaux mais {len(required)} valeurs fournies.")
            return
        if any(r <= 0 for r in required):
            messagebox.showerror("Erreur", "Tous les nombres doivent être positifs > 0.")
            return

        required_sorted = sorted(required, reverse=True)

        try:
            v = VLSMSimple()
            # Appel: (ip_depart, masque_cidr, nombre_sous_reseaux, liste_ips)
            results = v.calculer_vlsm(ip_depart, masque_cidr, nb_sr, required)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur pendant le calcul VLSM:\n{e}")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, subnet in enumerate(results):
            tag = 'evenrow' if i % 2 else 'oddrow'
            total_block = subnet.get('ips_utilisables', 0)
            self.tree.insert("", "end", values=(
                f"{subnet['reseau']}/{subnet['cidr']}",
                subnet['masque'],
                f"/{subnet['cidr']}",
                str(total_block),
                subnet['premiere_ip'],
                subnet['derniere_ip'],
                subnet['broadcast']
            ), tags=(tag,))
