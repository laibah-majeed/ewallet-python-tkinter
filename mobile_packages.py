import tkinter as tk
from tkinter import messagebox

class MobilePackages:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        
        # Mobile packages by network
        self.mobile_packages = {
            "Jazz": [
                ("Jazz Weekly (2GB, 100 mins)", 150),
                ("Jazz Monthly (10GB, 500 mins)", 500),
                ("Jazz Super (Unlimited GB, 1000 mins)", 1000)
            ],
            "Zong": [
                ("Zong Weekly (3GB, 150 mins)", 200),
                ("Zong Monthly (15GB, 750 mins)", 600),
                ("Zong Super (Unlimited GB, 1500 mins)", 1200)
            ],
            "Telenor": [
                ("Telenor Weekly (2.5GB, 120 mins)", 180),
                ("Telenor Monthly (12GB, 600 mins)", 550),
                ("Telenor Super (Unlimited GB, 1200 mins)", 1100)
            ],
            "Ufone": [
                ("Ufone Weekly (1.5GB, 80 mins)", 120),
                ("Ufone Monthly (8GB, 400 mins)", 450),
                ("Ufone Super (Unlimited GB, 800 mins)", 900)
            ]
        }
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_network_selection_screen(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Select Mobile Network", font=('Arial', 16)).pack(pady=10)
        
        networks_frame = tk.Frame(main_frame)
        networks_frame.pack(pady=20)
        
        networks = ["Jazz", "Zong", "Telenor", "Ufone"]
        
        for network in networks:
            tk.Button(networks_frame, text=network, 
                      command=lambda n=network: self.create_mobile_packages_screen(n)).pack(pady=5, fill=tk.X)
        
        tk.Button(main_frame, text="Back", command=self.return_to_main).pack(pady=20)
    
    def create_mobile_packages_screen(self, network):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text=f"{network} Packages", font=('Arial', 16)).pack(pady=10)
        tk.Label(main_frame, text=f"Current Balance: Rs.{self.current_user.balance:.2f}").pack(pady=5)
        
        form_frame = tk.Frame(main_frame)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Mobile Number (11 digits):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.mobile_number_entry = tk.Entry(form_frame)
        self.mobile_number_entry.grid(row=0, column=1, padx=5, pady=5)
        
        packages_frame = tk.Frame(main_frame)
        packages_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        for package, amount in self.mobile_packages[network]:
            pkg_frame = tk.Frame(packages_frame)
            pkg_frame.pack(pady=5, fill=tk.X, padx=50)
            
            tk.Label(pkg_frame, text=f"{package}: Rs.{amount:.2f}").pack(side=tk.LEFT)
            tk.Button(pkg_frame, text="Buy", 
                      command=lambda a=amount, p=package, n=network: self.confirm_package_purchase(a, p, n)).pack(side=tk.RIGHT)
        
        tk.Button(main_frame, text="Back", command=self.create_network_selection_screen).pack(pady=20)
    
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
    
    def confirm_package_purchase(self, amount, package_name, network):
        mobile_number = self.mobile_number_entry.get()
        if not mobile_number.isdigit() or len(mobile_number) != 11:
            messagebox.showerror("Error", "Invalid mobile number (must be 11 digits)")
            return
        
        self.ask_confirmation("Package Purchase", amount, 
                             f"Package: {package_name}\nNetwork: {network}\nMobile: {mobile_number}")
        
        if self.current_user.withdraw(amount):
            self.current_user.add_transaction(f"Purchased {package_name} ({network}) for {mobile_number}", amount)
            messagebox.showinfo("Success", f"{package_name} purchased successfully for {mobile_number}")
            self.return_to_main()
        else:
            messagebox.showerror("Error", "Insufficient balance")
    
    def return_to_main(self):
        self.clear_window()
        from user_manager import UserManager
        UserManager(self.root, self.current_user).create_main_menu()
