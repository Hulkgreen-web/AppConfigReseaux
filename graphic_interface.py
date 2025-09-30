import tkinter as tk
from tkinter import ttk, messagebox
from subnet import generer_plan_adressage_classique


class SubnetCalculatorApp:
    def __init__(self, master, ip_address, masque, nb_sr):
        self.master = master
        self.ip_address = ip_address
        self.masque = masque
        self.nb_sr = nb_sr
        master.title("Calculateur de Sous-Réseaux")
        master.geometry("1250x720")
        master.resizable(False, False)
        master.configure(background="#fcba03")

        frame_style = ttk.Style()
        frame_style.configure("TFrame", background="#fcba03")

        button_style = ttk.Style()
        button_style.configure("TButton", bg="#ba0404", font=("Arial", 15))

        # Frame pour les entrées
        input_frame = ttk.Frame(master, style="TFrame", padding="10")
        input_frame.pack(fill=tk.X)

        # Icone de l'application
        master.iconbitmap("ressources/logo.ico")

        # Adresse IP
        ttk.Label(input_frame, text="Adresse IP:", font=("arial",15),background="#ba0404", foreground="white").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ip_entry = ttk.Entry(input_frame, width=20, font=("arial", 15))
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ip_entry.insert(0, self.ip_address)

        # Masque
        ttk.Label(input_frame, text="Masque:", font=("arial",15),background="#ba0404", foreground="white").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.masque_entry = ttk.Entry(input_frame, width=20, font=("arial", 15))
        self.masque_entry.grid(row=0, column=3, padx=5, pady=5)
        self.masque_entry.insert(0, self.masque)

        # Nombre de sous-réseaux
        ttk.Label(input_frame, text="Nombre de Sous-Réseaux:", font=("arial",15),background="#ba0404", foreground="white").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.sr_entry = ttk.Entry(input_frame, width=10, font=("arial", 15))
        self.sr_entry.grid(row=0, column=5, padx=5, pady=5)
        self.sr_entry.insert(0, self.nb_sr)

        # Bouton de calcul
        ttk.Button(input_frame, text="Calculer", command=self.calculer_sous_reseaux).grid(row=0, column=6, padx=5,
                                                                                          pady=5)

        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background='#ba0404',
                        foreground='white',
                        font="arial",
                        borderwidth=1,
                        relief='solid',
                        rowheight=30)

        style.map("Custom.Treeview",
                  background=[('selected', '#fcba03')],
                  foreground=[('selected', 'white')])

        # Tableau pour afficher les résultats
        self.tree = ttk.Treeview(master,
                                 style="Custom.Treeview",
                                 columns=("Réseau", "Masque", "Nb Adresses", "Première IP", "Dernière IP", "Broadcast"),
                                 show="headings")

        # Définir les en-têtes
        self.tree.heading("Réseau", text="Réseau")
        self.tree.heading("Masque", text="Masque")
        self.tree.heading("Nb Adresses", text="Nombre total d'adresses")
        self.tree.heading("Première IP", text="Première IP utilisable")
        self.tree.heading("Dernière IP", text="Dernière IP utilisable")
        self.tree.heading("Broadcast", text="Adresse de broadcast")

        # Configurer la largeur des colonnes
        for col in self.tree["columns"]:
            self.tree.column(col, width=200, anchor=tk.CENTER)

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        btn_main_menu = ttk.Button(master, text="Retour au menu principal", command=self.open_main_menu)
        btn_main_menu.pack(padx=10, pady=10)

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
            for sr, details in plan.items():
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


    def open_main_menu(self):
        from menu_principal import MenuPrincipal

        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        MenuPrincipal(new_window)


