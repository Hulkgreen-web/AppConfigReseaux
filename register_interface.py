
from tkinter import *

class RegisterInterface:
    def __init__(self,master):
        self.master = master
        self.master.title("Register")
        self.master.geometry("1080x720")
        self.master.resizable(False, False)
        self.master.configure(background="#7529c2")

        label_title = Label(self.master, text="Register", font="arial 30 bold", fg="white", bg="#7529c2")
        label_title.pack(side=TOP)





def main():
    root = Tk()
    register_interface = RegisterInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()