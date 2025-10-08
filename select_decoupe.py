import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import get_decoupes_by_id
# Styles
BG = "#121212"        # fond principal
CARD_BG = "#f8fafc"   # carte
HEADER_BG = "#526787"
BTN_BG = "#6b7280"
BTN_FG = "white"
ACCENT = "#3b82f6"    # couleur accent si besoin
FONT = ("Segoe UI", 11)

class DecoupeSelector:
    def __init__(self,master, user_id):
        self.master = master
        self.user_id = user_id
        self.decoupes = []

        master.title("Sélection de découpe")
        master.geometry("1250x720")
        master.resizable(False, False)
        master.configure(bg=BG)

        # Card central
        card = tk.Frame(master, bg=CARD_BG)
        card.place(relx=0.5, rely=0.5, anchor="center", width=1180, height=660)

        # Header
        header = tk.Frame(card, bg=HEADER_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Sélection de découpe", bg=HEADER_BG, fg="white",
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=20)
        tk.Label(header, text=f"Utilisateur #{self.user_id}", bg=HEADER_BG, fg="#e6eef8",
                 font=("Segoe UI", 11)).pack(side="left", padx=12, pady=26)

        # Top info row
        info_row = tk.Frame(card, bg=CARD_BG)
        info_row.pack(fill="x", padx=18, pady=(12, 6))

        tk.Label(info_row, text="Découpe :", bg=CARD_BG, fg="#222", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.selected_name_lbl = tk.Label(info_row, text="(aucune sélection)", bg=CARD_BG, fg="#444", font=("Segoe UI", 12))
        self.selected_name_lbl.grid(row=0, column=1, sticky="w", padx=(6,20))

        # Boutons d'action
        btns = tk.Frame(info_row, bg=CARD_BG)
        btns.grid(row=0, column=4, sticky="e")
        btn_style = {"bg": BTN_BG, "fg": BTN_FG, "bd": 0, "padx": 12, "pady": 6, "font": FONT}
        tk.Button(btns, text="Retour", command=self.on_back, **btn_style).pack(side="left", padx=6)
        tk.Button(btns, text="Afficher", command=self.show_selected, **btn_style).pack(side="left", padx=6)
        tk.Button(btns, text="Rafraîchir", command=self.load_decoupes, **btn_style).pack(side="left", padx=6)

        # Table / list des découpes (Treeview)
        table_frame = tk.Frame(card, bg=CARD_BG)
        table_frame.pack(fill="both", expand=True, padx=18, pady=(6,12))

        cols = ("name",)
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=18)
        self.tree.heading("name", text="Nom de la découpe")
        self.tree.column("name", anchor="w", width=900, stretch=True)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Alternance de couleurs
        self.tree.tag_configure('oddrow', background='#ffffff')
        self.tree.tag_configure('evenrow', background='#f1f5f9')

        # Footer / statut
        footer = tk.Frame(card, bg=CARD_BG)
        footer.pack(fill="x", padx=18, pady=(0,12))
        self.status_lbl = tk.Label(footer, text="Prêt", bg=CARD_BG, fg="#666", font=("Segoe UI", 10))
        self.status_lbl.pack(side="left")

        # Appliquer style sur ttk via ttk.Style
        style = ttk.Style(master)
        style.theme_use('default')
        style.configure("Treeview",
                        background=CARD_BG,
                        fieldbackground=CARD_BG,
                        foreground="#111",
                        rowheight=28,
                        font=FONT)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=HEADER_BG, foreground="white")
        style.map("Treeview.Heading", background=[('active', HEADER_BG)])

        # Chargement initial
        self.load_decoupes()

        # Double-clic pour afficher
        self.tree.bind("<Double-1>", lambda e: self.show_selected())

    def load_decoupes(self):
        try:
            self.decoupes = get_decoupes_by_id(self.user_id) or []
            self.status_lbl.config(text=f"{len(self.decoupes)} découpes chargées")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les découpes :\n{e}")
            self.decoupes = []
            self.status_lbl.config(text="Erreur de chargement")

        # Mettre à jour la treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, name in enumerate(self.decoupes):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(name,), tags=(tag,))

        if not self.decoupes:
            self.selected_name_lbl.config(text="(aucune découpe)")
        else:
            self.selected_name_lbl.config(text=f"{len(self.decoupes)} disponibles")

    def show_selected(self):
        from load_data_interface import LoadedDecoupe
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Sélection", "Veuillez sélectionner une découpe.")
            return
        item = sel[0]
        name = self.tree.item(item, "values")[0]
        self.selected_name_lbl.config(text=name)
        self.status_lbl.config(text=f"Découpe sélectionnée : {name}")

        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        LoadedDecoupe(new_window, self.user_id, name)

    def on_back(self):
        from menu_principal import MenuPrincipal

        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        MenuPrincipal(new_window, self.user_id)
