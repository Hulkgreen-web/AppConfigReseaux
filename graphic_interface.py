import tkinter as tk
from tkinter import ttk, messagebox, Label

from subnet import generer_plan_adressage_classique
from db_utils import add_decoupe

class SubnetCalculatorApp:
    def __init__(self, master, ip_address="", masque="", nb_sr=0, user_id=0):
        self.master = master
        self.ip_address = ip_address
        self.masque = masque
        self.nb_sr = nb_sr
        self.user_id = user_id

        master.title("Calculateur de Sous-Réseaux")
        master.geometry("1250x720")
        master.resizable(False, False)
        master.configure(bg="#121212")  # fond sombre moderne

        # Card central
        card = tk.Frame(master, bg="#f8fafc", bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=1180, height=660)

        # Header
        header = tk.Frame(card, bg="#5a3bd6", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Calculateur de Sous-Réseaux", bg="#5a3bd6", fg="white",
                 font=("Segoe UI", 24, "bold")).pack(side="left", padx=20)
        tk.Label(header, text="Génère les sous-réseaux et leurs plages IP", bg="#5a3bd6",
                 fg="#e7e7ff", font=("Segoe UI", 11)).pack(side="left", padx=12, pady=28)

        # Input frame
        input_frame = tk.Frame(card, bg="#f8fafc")
        input_frame.pack(fill="x", padx=20, pady=(16, 8))

        lbl_ip = tk.Label(input_frame, text="Adresse IP:", bg="#f8fafc", fg="#222", font=("Segoe UI", 14))
        lbl_ip.grid(row=0, column=0, sticky="w")
        self.ip_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=18, justify="center", bd=1, relief="solid")
        self.ip_entry.grid(row=0, column=1, padx=8)
        self.ip_entry.insert(0, self.ip_address)
        self.ip_entry.config(state="disabled")

        lbl_mask = tk.Label(input_frame, text="Masque:", bg="#f8fafc", fg="#222", font=("Segoe UI", 14))
        lbl_mask.grid(row=0, column=2, sticky="w", padx=(20,0))
        self.masque_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=14, justify="center", bd=1, relief="solid")
        self.masque_entry.grid(row=0, column=3, padx=8)
        self.masque_entry.insert(0, self.masque)
        self.masque_entry.config(state="disabled")

        lbl_nb = tk.Label(input_frame, text="Nombre de SR:", bg="#f8fafc", fg="#222", font=("Segoe UI", 14))
        lbl_nb.grid(row=0, column=4, sticky="w", padx=(20,0))
        self.sr_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=8, justify="center", bd=1, relief="solid")
        self.sr_entry.grid(row=0, column=5, padx=8)
        self.sr_entry.insert(0, str(self.nb_sr))
        self.sr_entry.config(state="disabled")

        calc_btn = tk.Button(input_frame, text="Calculer", bg="#2b6cb0", fg="white", font=("Segoe UI", 13),
                             activebackground="#235a91", padx=16, pady=8, command=self.calculer_sous_reseaux)
        calc_btn.grid(row=0, column=6, padx=(30,0))

        # Tableau de résultats (Treeview) avec barre de défilement
        table_frame = tk.Frame(card, bg="#f8fafc")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(6, 12))

        cols = ("reseau", "masque", "nb", "premiere", "derniere", "broadcast")

        self.tree = ttk.Treeview(table_frame,columns=cols, show="headings", height=14)
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
            self.tree.column(c, anchor="center", width=180)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Pied de page avec boutons
        footer = tk.Frame(card, bg="#f8fafc")
        footer.pack(fill="x", padx=20, pady=(0,14))

        left_footer = tk.Frame(footer, bg="#f8fafc")
        left_footer.pack(side="left", anchor="w")

        info_lbl = tk.Label(left_footer, text=f"Utilisateur #{self.user_id}", bg="#f8fafc", fg="#666", font=("Segoe UI", 10))
        info_lbl.pack(side="left", padx=(0,12))

        save_btn = tk.Button(footer, text="Sauvegarder", bg="#16a34a", fg="white", font=("Segoe UI", 12),
                             activebackground="#13803d", padx=12, pady=8, command=self.save_on_db)
        save_btn.pack(side="right", padx=8)

        menu_btn = tk.Button(footer, text="Retour au menu principal", bg="#6b7280", fg="white", font=("Segoe UI", 12),
                             activebackground="#4b5563", padx=12, pady=8, command=self.open_main_menu)
        menu_btn.pack(side="right", padx=8)

        # Exemple de style visuel sur les lignes (alternance)
        self.tree.tag_configure('oddrow', background='#ffffff')
        self.tree.tag_configure('evenrow', background='#f1f5f9')

    def calculer_sous_reseaux(self):
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
            messagebox.showerror("Erreur", str(e))

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

    def save_on_db(self):
        try:
            adresse_ip = self.ip_entry.get()
            masque = self.masque_entry.get()
            nombre_sr = int(self.sr_entry.get())

            plan = generer_plan_adressage_classique(adresse_ip, masque, nombre_sr)

            response = custom_popup_entry("Sauvegarde", "Voulez-vous vraiment sauvegarder cette découpe ?")

            if (response is not None):
                add_decoupe(self.user_id,response,plan)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))


    def open_main_menu(self):
        from menu_principal import MenuPrincipal

        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        MenuPrincipal(new_window,self.user_id)

def custom_popup_entry(title,message):
    win = tk.Toplevel()
    win.title(title)
    custom_font = ("arial", 20)

    label_message = Label(win, text=message, font=custom_font)
    label_message.pack(padx=10, pady=10)

    name_entry = ttk.Entry(win, font=custom_font, justify=tk.LEFT)
    name_entry.pack(padx=10, pady=10)

    result = {"value": None}

    def on_ok():
        result["value"] = name_entry.get()
        win.destroy()
    def on_cancel():
        result["value"] = None
        win.destroy()

    btn_frame = ttk.Frame(win)
    btn_frame.pack(padx=10, pady=10)

    ok_btn = tk.Button(btn_frame, text="OK", command=on_ok, width=10)
    ok_btn.grid(row=0, column=0, padx=5)

    cancel_btn = tk.Button(btn_frame, text="Annuler", command=on_cancel, width=10)
    cancel_btn.grid(row=0, column=1, padx=5)

    win.transient()
    win.grab_set()
    win.wait_window()

    return result["value"]


