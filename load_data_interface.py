import tkinter as tk
from tkinter import ttk
from db_utils import get_decoupe_by_name, update_decoupe
from subnet import generer_plan_adressage_classique


class LoadedDecoupe:
    def __init__(self, master, user_id, decoupe_name, ip_entered, mask_entered, nb_sr_entered):
        self.master = master
        self.user_id = user_id
        self.decoupe_name = decoupe_name
        self.ip_entered = ip_entered
        self.mask_entered = mask_entered
        self.nb_sr_entered = nb_sr_entered

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

        save_btn = tk.Button(btns, text="Sauvegarder", bg="#16a34a", fg="white",
                             activebackground="#13803d", padx=10, pady=6, command=self.save_updated)
        save_btn.pack(side="right", padx=6)

        # Input frame
        input_frame = tk.Frame(card, bg="#f8fafc")
        input_frame.pack(fill="x", padx=20, pady=(16, 8))

        lbl_ip = tk.Label(input_frame, text="Adresse IP:", bg="#f8fafc", fg="#222", font=("Segoe UI", 14))
        lbl_ip.grid(row=0, column=0, sticky="w")
        self.ip_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=18, justify="center", bd=1, relief="solid")
        self.ip_entry.grid(row=0, column=1, padx=8)
        self.ip_entry.insert(0, self.ip_entered)

        lbl_mask = tk.Label(input_frame, text="Masque:", bg="#f8fafc", fg="#222", font=("Segoe UI", 14))
        lbl_mask.grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.masque_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=14, justify="center", bd=1,
                                     relief="solid")
        self.masque_entry.grid(row=0, column=3, padx=8)
        self.masque_entry.insert(0, self.mask_entered)

        lbl_nb = tk.Label(input_frame, text="Nombre de SR:", bg="#f8fafc", fg="#222", font=("Segoe UI", 14))
        lbl_nb.grid(row=0, column=4, sticky="w", padx=(20, 0))
        self.sr_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=8, justify="center", bd=1, relief="solid")
        self.sr_entry.grid(row=0, column=5, padx=8)
        self.sr_entry.insert(0, str(self.nb_sr_entered))

        calc_btn = tk.Button(input_frame, text="Modifier", bg="#2b6cb0", fg="white", font=("Segoe UI", 13),
                             activebackground="#235a91", padx=16, pady=8, command=self.update_subnet)
        calc_btn.grid(row=0, column=6, padx=(30, 0))

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

    def update_subnet(self):
        from register_interface import custom_messagebox, askyesno
        response = askyesno("Confirmation de la modification","Etes-vous sûr de vouloir modifier ce paramètre ?")
        if response:
            # Effacer les résultats précédents
            for i in self.tree.get_children():
                self.tree.delete(i)

            try:
                # Récupérer les valeurs des entrées
                adresse_ip = self.ip_entry.get()
                masque = self.masque_entry.get()
                nombre_sr = int(self.sr_entry.get())

                # Générer le plan d'adressage
                plan = generer_plan_adressage_classique(adresse_ip, masque, nombre_sr)

                # Remplir le tableau
                for i, details in plan.items():
                    self.tree.insert("", "end", values=(
                        details["Réseau"],
                        details["Masque"],
                        details["Nombre total d'adresses"],
                        details["Première IP utilisable"],
                        details["Dernière IP utilisable"],
                        details["Adresse de broadcast"]
                    ))

            except ValueError as e:
                custom_messagebox("Erreur", str(e))

            except Exception as e:
                custom_messagebox("Erreur", f"Une erreur est survenue : {str(e)}")

    def save_updated(self):
        from register_interface import custom_messagebox, askyesno
        try:
            adresse_ip = self.ip_entry.get()
            masque = self.masque_entry.get()
            nombre_sr = int(self.sr_entry.get())

            plan = generer_plan_adressage_classique(adresse_ip, masque, nombre_sr)

            response = askyesno("Confirmation", "Voulez-vous vraiment sauvegarder les changements ?")

            if response:
                update_decoupe(self.user_id, self.decoupe_name, adresse_ip, masque, nombre_sr,plan)
                custom_messagebox("Succès","Modification effectuée avec succès !")

        except Exception as e:
            custom_messagebox("Erreur", str(e))



    def return_to_last_menu(self):
        from select_decoupe import DecoupeSelector

        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        DecoupeSelector(new_window,self.user_id)