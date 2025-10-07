from tkinter import *

from db_utils import *
from load_data_interface import LoadedDecoupe


class RegisterInterface:
    def __init__(self,master):
        self.master = master
        self.master.title("S'inscrire")
        self.master.geometry("1080x720")
        self.master.resizable(False, False)
        self.master.configure(background="#121212")

        # Card central
        card = Frame(master, bg="#f7fafc")
        card.place(relx=0.5, rely=0.5, anchor="center", width=760, height=480)

        # Header
        header = Frame(card, bg="#526787", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        Label(header, text="S'inscrire", bg="#526787", fg="white",
              font=("Segoe UI", 26, "bold")).pack(side="left", padx=20)
        Label(header, text="Accédez à Network Manager", bg="#526787", fg="#e6eef8",
              font=("Segoe UI", 11)).pack(side="left", padx=12, pady=34)

        # Formulaire
        form = Frame(card, bg="#f7fafc")
        form.pack(expand=True)

        lbl_user = Label(form, text="Nom d'utilisateur", bg="#f7fafc", fg="#222", font=("Segoe UI", 14))
        lbl_user.grid(row=0, column=0, sticky="e", padx=(0, 12), pady=(8, 12))
        self.user_name_entry = Entry(form, font=("Segoe UI", 14), width=28, bd=1, relief="solid")
        self.user_name_entry.grid(row=0, column=1, pady=(8, 12))

        lbl_pwd = Label(form, text="Mot de passe", bg="#f7fafc", fg="#222", font=("Segoe UI", 14))
        lbl_pwd.grid(row=1, column=0, sticky="e", padx=(0, 12), pady=(0, 12))
        self.password_entry = Entry(form, show="*", font=("Segoe UI", 14), width=28, bd=1, relief="solid")
        self.password_entry.grid(row=1, column=1, pady=(0, 12))

        # Message d'erreur / info
        self.msg_label = Label(form, text="", bg="#f7fafc", fg="#b00020", font=("Segoe UI", 11))
        self.msg_label.grid(row=2, column=0, columnspan=2, pady=(4, 8))

        # Boutons
        btn_frame = Frame(card, bg="#f7fafc")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        register_btn = Button(btn_frame, text="S'inscrire", bg="#2b6cb0", fg="white",
                              font=("Segoe UI", 13, "bold"), bd=0, padx=20, pady=10,
                              command=self.register)
        register_btn.pack(side="left", padx=(0, 12))

        login_btn = Button(btn_frame, text="Se connecter", bg="#2b6cb0", fg="white",
                           font=("Segoe UI", 13, "bold"), bd=0, padx=20, pady=10,
                           command=self.open_login_interface)
        login_btn.pack(side="left", padx=(0, 12))


    def clear_form(self):
        self.user_name_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def register(self):
        username = self.user_name_entry.get()
        password = self.password_entry.get()
        user_choice = askyesno("Demande de confirmtion", "Etes-vous sûr de vous inscrire ?")
        if user_choice:
            response = add_user(username, password)
            if response:
                self.clear_form()
                custom_messagebox("Confirmation de l'inscription", f"Vous avez bien été inscrit {username}")
            else:
                custom_messagebox("Erreur", f"Ce nom d'utilisateur {username} existe déjà.")
        else:
            custom_messagebox("Annulation", "Inscription annulée")

    def open_login_interface(self):
        from login_interface import LoginInterface

        self.master.withdraw()
        new_window = Toplevel(self.master)
        LoginInterface(new_window)


def custom_messagebox(title, message):
    win = Toplevel()
    win.title(title)

    custom_font = ("arial", 20)

    label_message = Label(win, text=message,font=custom_font)
    label_message.pack()

    button_ok = Button(win, text="OK",font=custom_font, command=win.destroy)
    button_ok.pack(pady=10)

    win.transient()
    win.grab_set()
    win.wait_window()

def askyesno(title, message):
    win = Toplevel()
    win.title(title)
    win.resizable(False, False)

    custom_font = ("arial", 20)
    label_message = Label(win, text=message,font=custom_font)
    label_message.pack()

    result = {"value": None}

    def on_yes():
        result["value"] = True
        win.destroy()

    def on_no():
        result["value"] = False
        win.destroy()

    button_frame = Frame(win)
    button_frame.pack(pady=10)

    yes_btn = Button(button_frame, text="Oui", command=on_yes, width=10, font=("arial", 20))
    yes_btn.grid(row=0, column=0, padx=5)

    no_btn = Button(button_frame, text="Non", command=on_no, width=10, font=("arial", 20))
    no_btn.grid(row=0, column=1, padx=5)

    win.transient()
    win.grab_set()
    win.wait_window()

    return result["value"]