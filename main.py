from tkinter import Tk
from login_interface import LoginInterface


if __name__ == "__main__":
    root = Tk()
    app = LoginInterface(root)
    root.mainloop()