from tkinter import *
from db_utils import check_password, check_username, get_user_id
from register_interface import custom_messagebox

class LoginInterface:
    def __init__(self, master):
        self.master = master
        master.title("Se connecter")
        master.geometry("1080x720")
        master.resizable(False, False)
        master.configure(bg="#121212")  # fond sombre

        # Card central
        card = Frame(master, bg="#f7fafc")
        card.place(relx=0.5, rely=0.5, anchor="center", width=760, height=480)

        # Header
        header = Frame(card, bg="#526787", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        Label(header, text="Se connecter", bg="#526787", fg="white",
                 font=("Segoe UI", 26, "bold")).pack(side="left", padx=20)
        Label(header, text="Accédez à Network Manager", bg="#526787", fg="#e6eef8",
                 font=("Segoe UI", 11)).pack(side="left", padx=12, pady=34)

        # Formulaire
        form = Frame(card, bg="#f7fafc")
        form.pack(expand=True)

        lbl_user = Label(form, text="Nom d'utilisateur", bg="#f7fafc", fg="#222", font=("Segoe UI", 14))
        lbl_user.grid(row=0, column=0, sticky="e", padx=(0,12), pady=(8,12))
        self.user_name_entry = Entry(form, font=("Segoe UI", 14), width=28, bd=1, relief="solid")
        self.user_name_entry.grid(row=0, column=1, pady=(8,12))

        lbl_pwd = Label(form, text="Mot de passe", bg="#f7fafc", fg="#222", font=("Segoe UI", 14))
        lbl_pwd.grid(row=1, column=0, sticky="e", padx=(0,12), pady=(0,12))
        self.password_entry = Entry(form, show="*", font=("Segoe UI", 14), width=28, bd=1, relief="solid")
        self.password_entry.grid(row=1, column=1, pady=(0,12))

        # Message d'erreur / info
        self.msg_label = Label(form, text="", bg="#f7fafc", fg="#b00020", font=("Segoe UI", 11))
        self.msg_label.grid(row=2, column=0, columnspan=2, pady=(4,8))

        # Boutons
        btn_frame = Frame(card, bg="#f7fafc")
        btn_frame.pack(fill="x", padx=20, pady=(0,20))

        login_btn = Button(btn_frame, text="Connexion", bg="#2b6cb0", fg="white",
                              font=("Segoe UI", 13, "bold"), bd=0, padx=20, pady=10,
                              command=self.login)
        login_btn.pack(side="left", padx=(0,12))

        register_btn = Button(btn_frame, text="S'inscrire", bg="#2b6cb0", fg="white",
                              font=("Segoe UI", 13, "bold"), bd=0, padx=20, pady=10,
                              command=self.open_register_interface)
        register_btn.pack(side="left", padx=(0,12))

        help_btn = Button(btn_frame, text="Aide", bg="#e2e8f0", fg="#222",
                             font=("Segoe UI", 11), bd=0, padx=12, pady=8,
                             command=self.show_help)
        help_btn.pack(side="right")

        # Footer discret
        footer = Label(card, text="Mot de passe non mémorisé localement", bg="#f7fafc", fg="#666",
                          font=("Segoe UI", 10))
        footer.pack(side="bottom", pady=8)

    def login(self):
        user_from_db = check_username(self.user_name_entry.get())
        if user_from_db is None:
            custom_messagebox("Nom d'utilisateur invalide", "Nom d'utilisateur introuvable")
        password_from_db = check_password(user_from_db, self.password_entry.get())
        if password_from_db:
            custom_messagebox("Connexion effectuée", f"Vous êtes connecté {user_from_db}")
            self.open_main_menu(user_from_db)
        else:
            custom_messagebox("Mot de passe invalide", "Mot de passe invalide")

    def show_help(self):
        custom_messagebox("Aide", "Entrez votre nom d'utilisateur et mot de passe, puis cliquez sur Connexion.")

    def open_main_menu(self, user_name):
        from menu_principal import MenuPrincipal
        user_id = get_user_id(user_name)
        self.master.withdraw()
        new_window = Toplevel(self.master)
        MenuPrincipal(new_window, user_id)

    def open_register_interface(self):
        from register_interface import RegisterInterface

        self.master.withdraw()
        new_window = Toplevel(self.master)
        RegisterInterface(new_window)

'''def main():
    root = Tk()
    app = LoginInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()'''

