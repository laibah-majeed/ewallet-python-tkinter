from datetime import datetime
class User:
    def __init__(self, username, password, phone, balance=0.0):
        self.username = username
        self.password = password
        self.phone = phone  # 11-digit phone number
        self.balance = balance
        self.transaction_history = []
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.add_transaction("Deposit", amount)
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.add_transaction("Withdrawal", amount)
            return True
        return False
    
    def transfer(self, amount, recipient_phone, recipient_name="Unknown"):
        if self.withdraw(amount):
            self.add_transaction(f"Transfer to {recipient_phone}", amount)
            return True
        return False
    
    def add_transaction(self, description, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append({
            "timestamp": timestamp,
            "description": description,
            "amount": amount,
            "balance": self.balance
        })