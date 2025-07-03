import tkinter as tk

class TransactionHistory:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_transaction_history(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Transaction History", font=('Arial', 16)).pack(pady=10)
        
        if not self.current_user.transaction_history:
            tk.Label(main_frame, text="No transactions yet").pack(pady=20)
        else:
            history_frame = tk.Frame(main_frame)
            history_frame.pack(fill=tk.BOTH, expand=True)
            
            # Create a listbox with scrollbar
            scrollbar = tk.Scrollbar(history_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, width=100)
            listbox.pack(fill=tk.BOTH, expand=True)
            
            scrollbar.config(command=listbox.yview)
            
            # Add headers
            headers = "Date & Time".ljust(25) + "Description".ljust(40) + "Amount".rjust(15) + "Balance".rjust(15)
            listbox.insert(tk.END, headers)
            listbox.insert(tk.END, "-" * 95)
            
            # Add data to listbox
            for transaction in reversed(self.current_user.transaction_history):
                row = (f"{transaction['timestamp']}".ljust(25) + 
                       f"{transaction['description']}".ljust(40) + 
                       f"Rs.{transaction['amount']:.2f}".rjust(15) + 
                       f"Rs.{transaction['balance']:.2f}".rjust(15))
                listbox.insert(tk.END, row)
        
        tk.Button(main_frame, text="Back", command=self.return_to_main).pack(pady=20)
    
    def return_to_main(self):
        self.clear_window()
        from user_manager import UserManager
        UserManager(self.root, self.current_user).create_main_menu()