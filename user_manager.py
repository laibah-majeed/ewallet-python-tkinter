import tkinter as tk
from tkinter import messagebox
from user import User
from money_transfer import MoneyTransfer
from bill_payment import BillPayment
from mobile_packages import MobilePackages
from transaction_history import TransactionHistory

class UserManager:
    def __init__(self, root, current_user=None):
        self.root = root
        self.current_user = current_user
        
        # Sample users - now indexed by phone number
        self.users_by_phone = {
            "03123456789": User("alice", "pass123", "03123456789", 1500),
            "03987654321": User("bob", "pass456", "03987654321", 800)
        }
        self.users_by_name = {
            "alice": self.users_by_phone["03123456789"],
            "bob": self.users_by_phone["03987654321"]
        }
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_login_screen(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Welcome to MyE-Wallet", font=('Arial', 16)).pack(pady=20)
        
        form_frame = tk.Frame(main_frame)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.username_entry = tk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.password_entry = tk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Login", command=self.login).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Register", command=self.create_register_screen).pack(side=tk.LEFT, padx=10)
    
    def create_register_screen(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Create New Account", font=('Arial', 16)).pack(pady=20)
        
        form_frame = tk.Frame(main_frame)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_username_entry = tk.Entry(form_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_password_entry = tk.Entry(form_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Confirm Password:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_confirm_entry = tk.Entry(form_frame, show="*")
        self.reg_confirm_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Phone Number (11 digits):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.reg_phone_entry = tk.Entry(form_frame)
        self.reg_phone_entry.grid(row=3, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Register", command=self.register).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Back", command=self.create_login_screen).pack(side=tk.LEFT, padx=10)
    
    def create_main_menu(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, 
                 text=f"Welcome, {self.current_user.username}\nBalance: Rs.{self.current_user.balance:.2f}",
                 font=('Arial', 14)).pack(pady=20)
        
        menu_frame = tk.Frame(main_frame)
        menu_frame.pack(pady=10)
        
        buttons = [
            ("Deposit Money", self.create_deposit_screen),
            ("Send Money", lambda: MoneyTransfer(self.root, self.current_user, self.users_by_phone).create_transfer_screen()),
            ("Pay Bills", lambda: BillPayment(self.root, self.current_user).create_bill_reference_screen()),
            ("Mobile Packages", lambda: MobilePackages(self.root, self.current_user).create_network_selection_screen()),
            ("Transaction History", lambda: TransactionHistory(self.root, self.current_user).show_transaction_history()),
            ("Account Details", self.show_account_details),
            ("Logout", self.create_login_screen)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command).pack(pady=5, fill=tk.X)
    
    def create_deposit_screen(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Deposit Money", font=('Arial', 16)).pack(pady=10)
        tk.Label(main_frame, text=f"Current Balance: Rs.{self.current_user.balance:.2f}").pack(pady=5)
        
        form_frame = tk.Frame(main_frame)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Amount (Rs):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_entry = tk.Entry(form_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Deposit", command=self.confirm_deposit).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Back", command=self.create_main_menu).pack(side=tk.LEFT, padx=10)
    
    def show_account_details(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Account Details", font=('Arial', 16)).pack(pady=10)
        
        details_frame = tk.Frame(main_frame)
        details_frame.pack(pady=20)
        
        tk.Label(details_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(details_frame, text=self.current_user.username).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        tk.Label(details_frame, text="Phone Number:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(details_frame, text=self.current_user.phone).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        tk.Label(details_frame, text="Current Balance:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(details_frame, text=f"Rs.{self.current_user.balance:.2f}").grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        tk.Button(main_frame, text="Back", command=self.create_main_menu).pack(pady=20)
    
    def ask_confirmation(self, action, amount, recipient_info=""):
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Confirm Transaction")
        confirm_window.geometry("400x300")
        
        tk.Label(confirm_window, text=f"Confirm {action}", font=('Arial', 14)).pack(pady=10)
        
        details_frame = tk.Frame(confirm_window)
        details_frame.pack(pady=10)
        
        tk.Label(details_frame, text=f"Amount: Rs.{amount:.2f}").pack(anchor=tk.W)
        if recipient_info:
            tk.Label(details_frame, text=recipient_info).pack(anchor=tk.W)
        
        tk.Label(confirm_window, text="Enter your password to confirm:").pack(pady=10)
        
        password_entry = tk.Entry(confirm_window, show="*")
        password_entry.pack(pady=5)
        
        def verify_and_proceed():
            if password_entry.get() == self.current_user.password:
                confirm_window.destroy()
                return True
            else:
                messagebox.showerror("Error", "Incorrect password")
                return False
        
        btn_frame = tk.Frame(confirm_window)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Confirm", 
                  command=lambda: [verify_and_proceed() and confirm_window.grab_release() or None]).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancel", command=confirm_window.destroy).pack(side=tk.LEFT, padx=10)
        
        confirm_window.grab_set()
        confirm_window.wait_window()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.users_by_name and self.users_by_name[username].password == password:
            self.current_user = self.users_by_name[username]
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm = self.reg_confirm_entry.get()
        phone = self.reg_phone_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return
        
        if len(username) < 4:
            messagebox.showerror("Error", "Username must be at least 4 characters")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if not phone.isdigit() or len(phone) != 11:
            messagebox.showerror("Error", "Phone number must be 11 digits")
            return
        
        if phone in self.users_by_phone:
            messagebox.showerror("Error", "Phone number already registered")
            return
        
        if username in self.users_by_name:
            messagebox.showerror("Error", "Username already exists")
            return
        
        new_user = User(username, password, phone)
        self.users_by_phone[phone] = new_user
        self.users_by_name[username] = new_user
        
        messagebox.showinfo("Success", "Registration successful! Please login.")
        self.create_login_screen()
    
    def confirm_deposit(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
            
            self.ask_confirmation("Deposit", amount)
            
            if self.current_user.deposit(amount):
                messagebox.showinfo("Success", f"Deposited Rs.{amount:.2f} successfully")
                self.create_main_menu()
            else:
                messagebox.showerror("Error", "Invalid amount")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
