from tkinter import *

class MenuPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1080x720")
        self.master.resizable(False, False)
        self.master.configure(background="#fcba03")


        label_title = Label(master, text="Bienvenue dans Network Manager !",font=("Arial", 30) , fg="white", bg="#fcba03")
        label_title.pack(side=TOP, pady=50)

        btn_frame = Frame(self.master, bg="#fcba03")

        btn_find_network_information = Button(btn_frame, text="Calculer les caractéristiques réseaux de votre machine", font=("Arial", 20), fg="white", bg="#ba0404")
        btn_find_network_information.pack(pady=25, fill=X)

        btn_find_ip_address = Button(btn_frame, text="Vérifier l'appartenance d'une IP à votre réseaux", font=("Arial", 20), fg="white", bg="#ba0404")
        btn_find_ip_address.pack(pady=25, fill=X)

        btn_verif_cutting = Button(btn_frame, text="Vérifier la possibilité d'une découpe en sous-réseaux", font=("Arial", 20), fg="white", bg="#ba0404", command=self.open_graphic_interface)
        btn_verif_cutting.pack(pady=25, fill=X)

        btn_close_app = Button(btn_frame, text="Quitter l'application", font=("Arial", 20), fg="white", bg="#ba0404", command=master.quit)
        btn_close_app.pack(pady=25, fill=X)

        btn_frame.place(in_=master, anchor="c", relx=.5, rely=.5)

    def open_graphic_interface(self):
        # import local de la classe pour éviter
        # les problèmes d'import circulaire
        from graphic_interface import SubnetCalculatorApp

        self.master.withdraw()
        new_window = Toplevel(self.master)
        SubnetCalculatorApp(new_window)