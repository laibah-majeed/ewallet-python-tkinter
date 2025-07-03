import tkinter as tk
from tkinter import messagebox

class MoneyTransfer:
    def __init__(self, root, current_user, users_by_phone):
        self.root = root
        self.current_user = current_user
        self.users_by_phone = users_by_phone
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_transfer_screen(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Send Money", font=('Arial', 16)).pack(pady=10)
        tk.Label(main_frame, text=f"Current Balance: Rs.{self.current_user.balance:.2f}").pack(pady=5)
        
        form_frame = tk.Frame(main_frame)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Recipient Phone Number (11 digits):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.recipient_phone_entry = tk.Entry(form_frame)
        self.recipient_phone_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Amount (Rs):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.transfer_amount_entry = tk.Entry(form_frame)
        self.transfer_amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Send", command=self.confirm_transfer).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Back", command=self.return_to_main).pack(side=tk.LEFT, padx=10)
    
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
    
    def confirm_transfer(self):
        recipient_phone = self.recipient_phone_entry.get()
        
        if not recipient_phone.isdigit() or len(recipient_phone) != 11:
            messagebox.showerror("Error", "Invalid phone number (must be 11 digits)")
            return
        
        if recipient_phone == self.current_user.phone:
            messagebox.showerror("Error", "Cannot transfer to yourself")
            return
        
        try:
            amount = float(self.transfer_amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
            
            recipient_name = "Unknown"
            if recipient_phone in self.users_by_phone:
                recipient_name = self.users_by_phone[recipient_phone].username
            
            self.ask_confirmation("Transfer", amount, f"To: {recipient_phone} ({recipient_name})")
            
            if self.current_user.transfer(amount, recipient_phone, recipient_name):
                messagebox.showinfo("Success", f"Transferred Rs.{amount:.2f} to {recipient_phone}")
                self.return_to_main()
            else:
                messagebox.showerror("Error", "Insufficient balance")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def return_to_main(self):
        from user_manager import UserManager
        self.clear_window()
        UserManager(self.root, self.current_user).create_main_menu()