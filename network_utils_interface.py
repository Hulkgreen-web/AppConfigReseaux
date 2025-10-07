import tkinter as tk
from tkinter import Menu, Label, Entry, Radiobutton, StringVar, Text, END

from register_interface import custom_messagebox
from network_utils import *

class NetworkUtilsInterface:
    def __init__(self, master,user_id):
        self.master = master
        self.user_id = user_id
        self.master.title("Outils IP - calculate_network_info & check_ip_belongs")
        self.master.geometry("1080x500")
        self.master.resizable(False, False)
        self.master.configure(bg="#1f2933")  # fond sombre

        # Card central
        card = tk.Frame(master, bg="#f7fafc", bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=1020, height=460)

        # Header
        header = tk.Frame(card, bg="#526787", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Outils IP", bg="#526787", fg="white", font=("Segoe UI", 22, "bold")).pack(side="left", padx=20)
        tk.Label(header, text="calculate_network_info & check_ip_belongs", bg="#526787", fg="#e6eef8", font=("Segoe UI", 11)).pack(side="left", padx=8, pady=22)

        # Content
        content = tk.Frame(card, bg="#f7fafc")
        content.pack(fill="both", expand=True, padx=20, pady=12)

        # Ligne d'inputs (grande)
        inputs = tk.Frame(content, bg="#f7fafc")
        inputs.pack(fill="x", pady=(0,12))

        lbl_net = Label(inputs, text="IP / Réseau :", font=("Segoe UI", 14), bg="#f7fafc", fg="#222")
        lbl_net.grid(row=0, column=0, sticky="w", padx=(0,6), pady=6)
        self.entry_network_ip = Entry(inputs, font=("Segoe UI", 14), width=28)
        self.entry_network_ip.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        lbl_mask = Label(inputs, text="Masque (/24 ou 255.255.255.0) :", font=("Segoe UI", 14), bg="#f7fafc", fg="#222")
        lbl_mask.grid(row=0, column=2, sticky="w", padx=(20,6), pady=6)
        self.entry_mask = Entry(inputs, font=("Segoe UI", 14), width=20)
        self.entry_mask.grid(row=0, column=3, sticky="w", padx=6, pady=6)

        # Mode selection and buttons
        mid_row = tk.Frame(content, bg="#f7fafc")
        mid_row.pack(fill="x", pady=(0,12))

        lbl_mode = Label(mid_row, text="Mode :", font=("Segoe UI", 14), bg="#f7fafc", fg="#222")
        lbl_mode.grid(row=0, column=0, sticky="w", padx=(0,6))

        self.mode_var = StringVar(value='classless')
        rb1 = Radiobutton(mid_row, text="Classless", variable=self.mode_var, value='classless',
                          font=("Segoe UI", 13), bg="#f7fafc")
        rb1.grid(row=0, column=1, padx=6)
        rb2 = Radiobutton(mid_row, text="Classful", variable=self.mode_var, value='classful',
                          font=("Segoe UI", 13), bg="#f7fafc")
        rb2.grid(row=0, column=2, padx=6)

        # Boutons principaux (style simple)
        btn_frame = tk.Frame(mid_row, bg="#f7fafc")
        btn_frame.grid(row=0, column=3, sticky="e", padx=(40,0))
        btn_calc = tk.Button(btn_frame, text="Calculer réseau", font=("Segoe UI", 13), bg="#2b6cb0", fg="white",
                             activebackground="#235a91", padx=12, pady=8, command=self.on_calculate)
        btn_calc.pack(side="left", padx=8)
        btn_check = tk.Button(btn_frame, text="Vérifier appartenance IP", font=("Segoe UI", 13), bg="#526787", fg="white",
                              activebackground="#435f78", padx=12, pady=8, command=self.on_check)
        btn_check.pack(side="left", padx=8)

        # IP à tester
        test_row = tk.Frame(content, bg="#f7fafc")
        test_row.pack(fill="x", pady=(0,12))

        lbl_test = Label(test_row, text="IP à tester :", font=("Segoe UI", 14), bg="#f7fafc", fg="#222")
        lbl_test.grid(row=0, column=0, sticky="w")
        self.entry_ip_to_check = Entry(test_row, font=("Segoe UI", 14), width=24)
        self.entry_ip_to_check.grid(row=0, column=1, sticky="w", padx=8)

        # Résultats (grande zone)
        result_frame = tk.Frame(content, bg="#f7fafc")
        result_frame.pack(fill="both", expand=True)

        lbl_result = Label(result_frame, text="Résultats :", font=("Segoe UI", 14, "bold"), bg="#f7fafc", fg="#222")
        lbl_result.pack(anchor="w", padx=4, pady=(6,0))

        self.txt_results = Text(result_frame, font=("Segoe UI", 13), wrap="word", height=8, bg="white", fg="#111")
        self.txt_results.pack(fill="both", expand=True, padx=4, pady=8)
        self.txt_results.configure(state='disabled')

        # Footer
        footer = tk.Frame(card, bg="#f7fafc")
        footer.pack(fill="x", pady=(0,6))
        tk.Label(footer, text="Astuce: utilise 192.168.1.0 /24 comme exemple", bg="#f7fafc", fg="#666", font=("Segoe UI", 10)).pack(side="left", padx=8)
        tk.Button(footer, text="Effacer", command=self.clear_results, bg="#e53e3e", fg="white", bd=0, padx=10, pady=6).pack(side="right", padx=8)

        # Menu simple
        menubar = Menu(master)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Aide", command=self.show_help)
        menubar.add_cascade(label="Aide", menu=helpmenu)
        self.master.config(menu=menubar)

    def show_help(self):
        custom_messagebox("Aide", "Entrez une IP/réseau, un masque (ex: /24 ou 255.255.255.0). Choisissez le mode et cliquez sur un bouton.")

    def write_result(self, text):
        self.txt_results.configure(state='normal')
        self.txt_results.delete(1.0, END)
        self.txt_results.insert(END, text)
        self.txt_results.configure(state='disabled')

    def on_calculate(self):
        try:
            ip = self.entry_network_ip.get().strip()
            mask = self.entry_mask.get().strip()
            mode = self.mode_var.get()
            if not ip or not mask:
                custom_messagebox("Erreur", "IP et masque requis pour le calcul.")
                return
            res = calculate_network_info(ip, mask, mode)
            if 'erreur' in res:
                self.write_result(f"Erreur: {res['erreur']}")
                return
            out = []
            out.append(f"Mode: {mode}")
            out.append(f"Adresse réseau: {res.get('adresse réseau')}")
            out.append(f"Broadcast: {res.get('adresse de brocast')}")
            out.append(
                f"Masque de sous-réseau: {res.get('masque de sous reseau') or res.get('masque de sous réseau') or res.get('netmask')}")
            out.append(f"Subnet: {res.get('subnet')}")
            self.write_result("\n".join(out))
        except Exception as e:
            custom_messagebox("Erreur", e)

    def on_check(self):
        network_ip = self.entry_network_ip.get().strip()
        mask = self.entry_mask.get().strip()
        ip_to_check = self.entry_ip_to_check.get().strip()
        mode = self.mode_var.get()
        if not network_ip or not mask or not ip_to_check:
            custom_messagebox("Erreur", "IP réseau, masque et IP à tester sont requis.")
            return
        res = check_ip_belongs(ip_to_check, network_ip, mask, mode)
        if 'error' in res:
            self.write_result(f"Erreur: {res['error']}")
            return
        out = []
        out.append(f"Mode: {mode}")
        out.append(f"L'IP {ip_to_check} appartient au réseau: {res.get('appartient')}")
        out.append(f"Premier hôte: {res.get('premier hote')}")
        out.append(f"Dernier hôte: {res.get('dernier hote')}")
        self.write_result("\n".join(out))

    def clear_results(self):
        self.txt_results.configure(state='normal')
        self.txt_results.delete("1.0", END)
        self.txt_results.configure(state='disabled')