import tkinter as tk
from tkinter import messagebox

class BillPayment:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        
        # Bill types with their reference numbers
        self.bill_types = {
            "Electricity Bill": {
                "ref1": "ELEC123456",
                "ref2": "ELEC789012",
                "amount": 1200.50
            },
            "Water Bill": {
                "ref1": "WATER12345",
                "ref2": "WATER67890",
                "amount": 850.75
            },
            "Gas Bill": {
                "ref1": "GAS1234567",
                "ref2": "GAS8901234",
                "amount": 1450.25
            },
            "Internet Bill": {
                "ref1": "NET1234567",
                "ref2": "NET7654321",
                "amount": 1650.00
            },
            "Credit Card Payment": {
                "ref1": "CC12345678",
                "ref2": "CC87654321",
                "amount": 2000.00
            }
        }
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_bill_reference_screen(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Enter Bill Reference Number", font=('Arial', 16)).pack(pady=10)
        tk.Label(main_frame, text=f"Current Balance: Rs.{self.current_user.balance:.2f}").pack(pady=5)
        
        form_frame = tk.Frame(main_frame)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Reference Number:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.bill_ref_entry = tk.Entry(form_frame)
        self.bill_ref_entry.grid(row=0, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Continue", command=self.check_bill_reference).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Back", command=self.return_to_main).pack(side=tk.LEFT, padx=10)
    
    def check_bill_reference(self):
        ref_number = self.bill_ref_entry.get()
        if not ref_number:
            messagebox.showerror("Error", "Please enter a reference number")
            return
        
        # Check which bill this reference number belongs to
        matched_bill = None
        for bill_name, bill_data in self.bill_types.items():
            if ref_number in [bill_data["ref1"], bill_data["ref2"]]:
                matched_bill = (bill_name, bill_data["amount"])
                break
        
        if matched_bill:
            self.show_bill_payment_screen(matched_bill[0], matched_bill[1], ref_number)
        else:
            messagebox.showerror("Error", "Invalid reference number")
    
    def show_bill_payment_screen(self, bill_name, amount, ref_number):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Pay Bill", font=('Arial', 16)).pack(pady=10)
        tk.Label(main_frame, text=f"Current Balance: Rs.{self.current_user.balance:.2f}").pack(pady=5)
        
        details_frame = tk.Frame(main_frame)
        details_frame.pack(pady=20)
        
        tk.Label(details_frame, text=f"Bill Type: {bill_name}").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(details_frame, text=f"Amount: Rs.{amount:.2f}").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(details_frame, text=f"Reference Number: {ref_number}").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Pay Now", 
                  command=lambda: self.confirm_bill_payment(amount, bill_name, ref_number)).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Back", command=self.create_bill_reference_screen).pack(side=tk.LEFT, padx=10)
    
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
        
        tk.Button(btn_frame, text="Confirm", command=lambda: [verify_and_proceed() and confirm_window.grab_release() or None]).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancel", command=confirm_window.destroy).pack(side=tk.LEFT, padx=10)
        
        confirm_window.grab_set()
        confirm_window.wait_window()
    
    def confirm_bill_payment(self, amount, bill_name, ref_number):
        self.ask_confirmation("Bill Payment", amount, f"Bill: {bill_name}\nRef: {ref_number}")
        
        # Modified to only record one transaction
        if 0 < amount <= self.current_user.balance:
            self.current_user.balance -= amount
            self.current_user.add_transaction(f"Paid {bill_name} (Ref: {ref_number})", amount)
            messagebox.showinfo("Success", f"{bill_name} paid successfully")
            self.return_to_main()
        else:
            messagebox.showerror("Error", "Insufficient balance")
    
    def return_to_main(self):
        self.clear_window()
        from user_manager import UserManager
        UserManager(self.root, self.current_user).create_main_menu()