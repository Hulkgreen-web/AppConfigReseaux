import tkinter as tk
from tkinter import ttk
from db_utils import get_decoupe_by_name

class LoadedDecoupe:
    def __init__(self, master):
        self.master = master
        self.user_id = 2
        self.decoupe_name = "decoupe_tri"

        master.title("Visualisation de découpe")
        master.geometry("1250x720")
        master.resizable(False, False)
        master.configure(background="#989a9e")

        frame_style = ttk.Style()
        frame_style.configure("TFrame", background="#989a9e")

        button_style = ttk.Style()
        button_style.configure("TButton", bg="#526787", font=("Arial", 15))

        # Frame pour les entrées
        input_frame = ttk.Frame(master, style="TFrame", padding="10")
        input_frame.pack(fill=tk.X)

        # Icone de l'application
        master.iconbitmap("ressources/logo.ico")

        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background='#526787',
                        foreground='white',
                        font="arial",
                        borderwidth=1,
                        relief='solid',
                        rowheight=30)

        style.map("Custom.Treeview",
                  background=[('selected', '#989a9e')],
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

        '''btn_main_menu = ttk.Button(master, text="Retour au menu principal", command=self.open_main_menu)
        btn_main_menu.pack(padx=10, pady=10)'''

        # Charger les données et les placer dans le tableau
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

def main():
    root = tk.Tk()
    app = LoadedDecoupe(root)
    root.mainloop()

if __name__ == "__main__":
    main()