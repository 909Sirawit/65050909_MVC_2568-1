#console view
# from controller.controller import Controller
# from view.view import View

# if __name__ == "__main__":
#     ctrl = Controller()
#     View.login(ctrl) 
#     View.show_menu(ctrl)


# gui (main view from now)
from view.view_gui import JobApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = JobApp(root)
    root.mainloop()

