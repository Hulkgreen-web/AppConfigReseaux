from tkinter import *

from db_utils import *

class RegisterInterface:
    def __init__(self,master):
        self.master = master
        self.master.title("Register")
        self.master.geometry("1080x720")
        self.master.resizable(False, False)
        self.master.configure(background="#989a9e")

        label_title = Label(self.master, text="S'inscrire", font="arial 30 bold", fg="white", bg="#989a9e")
        label_title.pack(side=TOP, pady=50)

        register_form_frame = Frame(self.master, bg="#989a9e", padx=10, pady=6)

        label_user_name = Label(register_form_frame, text="Nom d'utilisateur : ",font= "arial 20", fg="white", bg="#989a9e")
        label_user_name.grid(row=0, column=0, sticky=E)

        self.user_name_entry = Entry(register_form_frame, font=("arial",20), background="#296ec2", foreground="white")
        self.user_name_entry.grid(row=0, column=1, pady=100)

        label_password = Label(register_form_frame, text="Mot de passe : ", font="arial 20", fg="white", bg="#989a9e")
        label_password.grid(row=1, column=0, sticky=E)

        self.password_entry = Entry(register_form_frame,show="*", font=("arial",20), background="#296ec2", foreground="white")
        self.password_entry.grid(row=1, column=1)

        btn_confirm_register = Button(master, text="Confirmer l'inscription", font="arial, 20", command=self.register)
        btn_confirm_register.pack(side=BOTTOM, pady=50)


        register_form_frame.pack()


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

def main():
    root = Tk()
    register_interface = RegisterInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()