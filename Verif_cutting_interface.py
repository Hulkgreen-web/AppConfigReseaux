import tkinter as tk
from Verif_cutting import *
from register_interface import custom_messagebox, askyesno

class VerificateurDecoupe:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id

        # --- Fenêtre principale ---
        master.title("Outil de découpe réseau")
        master.geometry("1250x500")
        master.minsize(1250, 500)
        master.configure(bg="#989a9e")

        # Styles
        style = ttk.Style(master)
        style.configure("TLabelframe.Label", font=("Arial", 16, "bold"))
        style.configure("TLabel", font=("Arial", 14))
        style.configure("TEntry", font=("Arial", 13))
        style.configure("TButton", font=("Arial", 13))

        # Container principal avec padding
        container = ttk.Frame(master, padding=20)
        container.pack(fill="both", expand=True)

        # deux colonnes dans container
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        # --- Découpe classique (gauche) ---
        frame1 = ttk.LabelFrame(container, text="Découpe classique", padding=20)
        frame1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        for i in range(2):
            frame1.columnconfigure(i, weight=1)

        ttk.Label(frame1, text="Adresse IP de base :").grid(row=0, column=0, sticky="e", padx=8, pady=8)
        self.entry_ip = ttk.Entry(frame1, font=("Arial", 14))
        self.entry_ip.grid(row=0, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(frame1, text="Masque (ex: 255.255.255.0) :").grid(row=1, column=0, sticky="e", padx=8, pady=8)
        self.entry_masque = ttk.Entry(frame1, font=("Arial", 14))
        self.entry_masque.grid(row=1, column=1, sticky="ew", padx=8, pady=8)

        self.var_choix = tk.IntVar(value=1)
        rb1 = ttk.Radiobutton(frame1, text="Nombre de sous-réseaux", variable=self.var_choix, value=1)
        rb1.grid(row=2, column=0, sticky="w", padx=8, pady=8)
        self.entry_nb_sr = ttk.Entry(frame1)
        self.entry_nb_sr.grid(row=2, column=1, sticky="ew", padx=8, pady=8)

        rb2 = ttk.Radiobutton(frame1, text="Nombre d'IPs par SR", variable=self.var_choix, value=2)
        rb2.grid(row=3, column=0, sticky="w", padx=8, pady=8)
        self.entry_nb_ips = ttk.Entry(frame1)
        self.entry_nb_ips.grid(row=3, column=1, sticky="ew", padx=8, pady=8)

        btn_verif = ttk.Button(frame1, text="Vérifier", command=self.calculer_classique)
        btn_verif.grid(row=4, column=0, columnspan=2, pady=12, ipadx=10)

        # --- VLSM (droite) ---
        frame2 = ttk.LabelFrame(container, text="Vérification VLSM", padding=20)
        frame2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        for i in range(2):
            frame2.columnconfigure(i, weight=1)

        ttk.Label(frame2, text="Adresse IP de base :").grid(row=0, column=0, sticky="e", padx=8, pady=8)
        self.entry_ip_vlsm = ttk.Entry(frame2, font=("Arial", 14))
        self.entry_ip_vlsm.grid(row=0, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(frame2, text="Masque (ex: /24) :").grid(row=1, column=0, sticky="e", padx=8, pady=8)
        self.entry_masque_vlsm = ttk.Entry(frame2, font=("Arial", 14))
        self.entry_masque_vlsm.grid(row=1, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(frame2, text="Besoins en IPs par SR (ex: 50,20,10) :").grid(row=2, column=0, sticky="e", padx=8, pady=8)
        self.entry_besoins = ttk.Entry(frame2, font=("Arial", 14))
        self.entry_besoins.grid(row=2, column=1, sticky="ew", padx=8, pady=8)

        btn_vlsm = ttk.Button(frame2, text="Vérifier VLSM", command=self.calculer_vlsm)
        btn_vlsm.grid(row=3, column=0, columnspan=2, pady=12, ipadx=10)

        # --- Boutons bas ---
        bottom_frame = ttk.Frame(master, padding=10)
        bottom_frame.pack(side="bottom", fill="x")
        btn_return = ttk.Button(bottom_frame, text="Retour au menu principal", command=self.open_main_menu)
        btn_return.pack(side="right", padx=20)

    # --- Interface graphique ---
    def calculer_classique(self):
        ip = self.entry_ip.get()
        masque = self.entry_masque.get()
        choix = self.var_choix.get()
        if choix == 1:
            try:
                nb_sr = int(self.entry_nb_sr.get())
            except:
                custom_messagebox("Erreur", "Nombre de sous-réseaux invalide.")
                return
            ok, msg = verifier_decoupe_classique(ip, masque, nb_sr=nb_sr)
            if ok:
                custom_messagebox("Résultat", msg)
                reponse = askyesno("Proposition de découpe", "Voulez-vous effectuer la découpe classique ?")
                if reponse:
                    self.open_graphic_interface(ip, masque, nb_sr=nb_sr)
                else:
                    custom_messagebox("Annulation de découpe", "Découpe classique annulée")
            else:
                custom_messagebox("Erreur", msg)
        else:
            try:
                nb_ips = int(self.entry_nb_ips.get())
            except:
                custom_messagebox("Erreur", "Nombre d'IPs invalide.")
                return
            ok, msg, nb_sr_possible = verifier_decoupe_classique(ip, masque, nb_ips_par_sr=nb_ips)
            if ok:
                custom_messagebox("Résultat", msg)
                reponse = askyesno("Proposition de découpe", "Voulez-vous effectuer la découpe classique ?")
                if reponse:
                    self.open_graphic_interface(ip, masque, nb_sr=nb_sr_possible)
                else:
                    custom_messagebox("Annulation de découpe", "Découpe classique annulée")
            else:
                custom_messagebox("Erreur", msg)

    def calculer_vlsm(self):
        ip = self.entry_ip_vlsm.get()
        masque = self.entry_masque_vlsm.get()
        besoins_str = self.entry_besoins.get()
        try:
            besoins = [int(x) for x in besoins_str.split(",")]
        except:
            messagebox.showerror("Erreur", "Liste des besoins invalide (ex: 50,20,10)")
            return
        ok, msg = verifier_vlsm_possible(ip, masque, besoins)
        if ok:
            messagebox.showinfo("Résultat", msg)
        else:
            messagebox.showerror("Erreur", msg)

    def open_main_menu(self):
        from menu_principal import MenuPrincipal

        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        MenuPrincipal(new_window,self.user_id)

    def open_graphic_interface(self,ip_address,masque,nb_sr):
        # import local de la classe pour éviter
        # les problèmes d'import circulaire
        from graphic_interface import SubnetCalculatorApp

        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        SubnetCalculatorApp(new_window,ip_address,masque,nb_sr,self.user_id)