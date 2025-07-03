import tkinter as tk
from user_manager import UserManager

class EWalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MyE-Wallet")
        self.root.geometry("650x550")
        self.user_manager = UserManager(root)
        self.user_manager.create_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = EWalletApp(root)
    root.mainloop()
