from tkinter import *
from db_utils import check_password, check_username
from register_interface import custom_messagebox

class LoginInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Se connecter")
        self.master.geometry("1080x720")
        self.master.resizable(width=False, height=False)
        self.master.configure(background="#989a9e")

        label_title = Label(self.master, text="Se connecter", font="arial 30 bold", fg="white", bg="#989a9e")
        label_title.pack(side=TOP, pady=50)

        login_form_frame = Frame(self.master, bg="#989a9e", padx=10, pady=6)

        label_user_name = Label(login_form_frame, text="Nom d'utilisateur : ", font="arial 20", fg="white",
                                bg="#989a9e")
        label_user_name.grid(row=0, column=0, sticky=E)

        self.user_name_entry = Entry(login_form_frame, font=("arial", 20), background="#526787", foreground="white")
        self.user_name_entry.grid(row=0, column=1, pady=100)

        label_password = Label(login_form_frame, text="Mot de passe : ", font="arial 20", fg="white", bg="#989a9e")
        label_password.grid(row=1, column=0, sticky=E)

        self.password_entry = Entry(login_form_frame, show="*", font=("arial", 20), background="#526787",
                                    foreground="white")
        self.password_entry.grid(row=1, column=1)

        btn_confirm_login = Button(master, text="Connexion", font="arial, 20",bg="#526787",fg="white", command=self.login)
        btn_confirm_login.pack(side=BOTTOM, pady=50)

        login_form_frame.pack()

    def login(self):
        user_from_db = check_username(self.user_name_entry.get())
        if user_from_db is None:
            custom_messagebox("Nom d'utilisateur invalide", "Nom d'utilisateur introuvable")
        password_from_db = check_password(user_from_db, self.password_entry.get())
        if password_from_db:
            custom_messagebox("Connexion effectuée", f"Vous êtes connecté {user_from_db}")
            self.open_main_menu()
        else:
            custom_messagebox("Mot de passe invalide", "Mot de passe invalide")

    def open_main_menu(self):
        from menu_principal import MenuPrincipal

        self.master.withdraw()
        new_window = Toplevel(self.master)
        MenuPrincipal(new_window)

def main():
    root = Tk()
    app = LoginInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()

