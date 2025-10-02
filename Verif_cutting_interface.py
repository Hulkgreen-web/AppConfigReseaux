import tkinter as tk
from tkinter import ttk, messagebox
from Verif_cutting import *

class VerificateurDecoupe:
    def __init__(self, master):
        self.master = master
        # --- Fenêtre principale avec thème et fond ---
        master.title("Outil de découpe réseau")
        master.geometry("500x450")
        master.configure(bg="#989a9e")

        # --- Découpe classique ---
        frame1 = ttk.LabelFrame(master, text="Découpe classique", padding=10,)
        frame1.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame1, text="Adresse IP de base :", font=("arial",15)).grid(row=0, column=0, sticky="e")
        self.entry_ip = tk.Entry(frame1, )
        self.entry_ip.grid(row=0, column=1)

        ttk.Label(frame1, text="Masque (ex: 24 ou 255.255.255.0) :", font=("arial",15)).grid(row=1, column=0, sticky="e")
        self.entry_masque = tk.Entry(frame1, )
        self.entry_masque.grid(row=1, column=1)

        self.var_choix = tk.IntVar(value=1)
        ttk.Radiobutton(frame1, text="Nombre de sous-réseaux", variable=self.var_choix, value=1).grid(row=2, column=0,
                                                                                                 sticky="w")
        self.entry_nb_sr = tk.Entry(frame1, )
        self.entry_nb_sr.grid(row=2, column=1)

        ttk.Radiobutton(frame1, text="Nombre d'IPs par SR", variable=self.var_choix, value=2).grid(row=3, column=0,
                                                                                              sticky="w")
        self.entry_nb_ips = tk.Entry(frame1, )
        self.entry_nb_ips.grid(row=3, column=1)

        ttk.Button(frame1, text="Vérifier", command=self.calculer_classique).grid(row=4, column=0, columnspan=2, pady=5)

        # --- VLSM ---
        frame2 = ttk.LabelFrame(master, text="Vérification VLSM", padding=10)
        frame2.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame2, text="Adresse IP de base :").grid(row=0, column=0, sticky="e")
        self.entry_ip_vlsm = tk.Entry(frame2, )
        self.entry_ip_vlsm.grid(row=0, column=1)

        ttk.Label(frame2, text="Masque (ex: 24 ou 255.255.255.0) :").grid(row=1, column=0, sticky="e")
        self.entry_masque_vlsm = tk.Entry(frame2, )
        self.entry_masque_vlsm.grid(row=1, column=1)

        ttk.Label(frame2, text="Besoins en IPs par SR (ex: 50,20,10) :").grid(row=2, column=0, sticky="e")
        self.entry_besoins = tk.Entry(frame2, )
        self.entry_besoins.grid(row=2, column=1)

        ttk.Button(frame2, text="Vérifier VLSM", command=self.calculer_vlsm).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(master, text="Retour au menu principal", command=self.open_main_menu).pack(side="bottom")

    # --- Interface graphique ---
    def calculer_classique(self):
        ip = self.entry_ip.get()
        masque = self.entry_masque.get()
        choix = self.var_choix.get()
        if choix == 1:
            try:
                nb_sr = int(self.entry_nb_sr.get())
            except:
                messagebox.showerror("Erreur", "Nombre de sous-réseaux invalide.")
                return
            ok, msg = verifier_decoupe_classique(ip, masque, nb_sr=nb_sr)
            if ok:
                messagebox.showinfo("Résultat", msg)
                reponse = messagebox.askyesno("Proposition de découpe", "Voulez-vous effectuer la découpe classique ?")
                if reponse:
                    self.open_graphic_interface(ip, masque, nb_sr=nb_sr)
                else:
                    messagebox.showinfo("Annulation de découpe", "Découpe classique annulée")
            else:
                messagebox.showerror("Erreur", msg)
        else:
            try:
                nb_ips = int(self.entry_nb_ips.get())
            except:
                messagebox.showerror("Erreur", "Nombre d'IPs invalide.")
                return
            ok, msg, nb_sr_possible = verifier_decoupe_classique(ip, masque, nb_ips_par_sr=nb_ips)
            if ok:
                messagebox.showinfo("Résultat", msg)
                reponse = messagebox.askyesno("Proposition de découpe", "Voulez-vous effectuer la découpe classique ?")
                if reponse:
                    self.open_graphic_interface(ip, masque, nb_sr=nb_sr_possible)
                else:
                    messagebox.showinfo("Annulation de découpe", "Découpe classique annulée")
            else:
                messagebox.showerror("Erreur", msg)

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
        MenuPrincipal(new_window)

    def open_graphic_interface(self,ip_address,masque,nb_sr):
        # import local de la classe pour éviter
        # les problèmes d'import circulaire
        from graphic_interface import SubnetCalculatorApp

        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        SubnetCalculatorApp(new_window,ip_address,masque,nb_sr)