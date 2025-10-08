from tkinter import *

class MenuPrincipal:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id

        # fenêtre
        master.geometry("1080x720")
        master.title("Menu principal")
        master.resizable(False, False)
        master.config(bg="#1f2933")  # fond sombre moderne

        # conteneur central
        card = Frame(master, bg="#f7fafc", bd=0, relief="flat")
        card.place(relx=0.5, rely=0.5, anchor="center", width=920, height=560)

        # en-tête du "card"
        header = Frame(card, bg="#526787", height=110)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = Label(header, text="Network Manager", bg="#526787", fg="white",
                         font=("Segoe UI", 28, "bold"))
        title.pack(side="left", padx=24)

        subtitle = Label(header, text="Outils de diagnostic et découpe réseau", bg="#526787",
                            fg="#e6eef8", font=("Segoe UI", 12))
        subtitle.pack(side="left", padx=12, pady=36)

        # zone de contenu
        content = Frame(card, bg="#f7fafc")
        content.pack(fill="both", expand=True, padx=30, pady=20)

        # colonne gauche : description + icône
        left = Frame(content, bg="#f7fafc")
        left.pack(side="left", fill="y", expand=False)

        # petite illustration (optionnelle)
        try:
            # remplace "network.png" par un chemin réel si tu veux une image
            img = PhotoImage(file="ressources/logo.ico")
            icon = Label(left, image=img, bg="#f7fafc")
            icon.image = img
            icon.pack(pady=6, padx=6)
        except Exception:
            logo = Canvas(left, width=140, height=140, bg="#f7fafc", highlightthickness=0)
            logo.create_oval(10,10,130,130, fill="#526787", outline="")
            logo.create_text(70,80, text="NM", fill="white", font=("Segoe UI", 28, "bold"))
            logo.pack(pady=6, padx=6)

        desc = Label(left, text="Analysez et planifiez vos réseaux\nrapidement et simplement.",
                        bg="#f7fafc", fg="#333", font=("Segoe UI", 12), justify="left")
        desc.pack(padx=8, pady=8)

        # colonne droite : boutons
        right = Frame(content, bg="#f7fafc")
        right.pack(side="right", fill="both", expand=True)

        # style bouton helper
        def make_btn(parent, text, command=None, accent=False):
            bg = "#526787" if not accent else "#2b6cb0"
            hover = "#435f78" if not accent else "#235a91"
            btn_container = Frame(parent, bg=bg, height=72)
            btn_container.pack(fill="x", pady=12)
            btn_container.pack_propagate(False)

            btn = Button(btn_container, text=text, bg=bg, fg="white",
                            font=("Segoe UI", 16), bd=0, activebackground=hover,
                            activeforeground="white", cursor="hand2", command=command)
            btn.pack(fill="both", expand=True, padx=6, pady=6)

            # effet hover
            def on_enter(e):
                btn.config(bg=hover)
                btn_container.config(bg=hover)
            def on_leave(e):
                btn.config(bg=bg)
                btn_container.config(bg=bg)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

            return btn

        make_btn(right, "Calculer les caractéristiques réseaux de votre machine", command=self.open_network_utils_interface)
        make_btn(right, "Vérifier la possibilité d'une découpe en sous-réseaux", command=self.open_graphic_interface)
        make_btn(right, "Consulter les données sauvegardées", command=self.open_select_decoupe)
        make_btn(right, "Quitter l'application", command=master.quit)

    def open_select_decoupe(self):
        from select_decoupe import DecoupeSelector

        self.master.withdraw()
        new_window = Toplevel(self.master)
        DecoupeSelector(new_window,self.user_id)

    def open_network_utils_interface(self):
        from network_utils_interface import NetworkUtilsInterface

        self.master.withdraw()
        new_window = Toplevel(self.master)
        NetworkUtilsInterface(new_window,self.user_id)

    def open_graphic_interface(self):
        # import local de la classe pour éviter
        # les problèmes d'import circulaire
        from Verif_cutting_interface import VerificateurDecoupe

        self.master.withdraw()
        new_window = Toplevel(self.master)
        VerificateurDecoupe(new_window,self.user_id)