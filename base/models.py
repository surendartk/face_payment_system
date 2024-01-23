from django.db import models

# Create your models here.
from django.db import models

class BankAccount(models.Model):
    username = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transactions = models.TextField(default="[]")  # Store transactions as JSON string

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposit: +${amount}")
            self.save()
            return f"Deposit of ${amount} successful. New balance: ${self.balance}"
        else:
            return "Invalid deposit amount. Please enter a positive value."

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: -${amount}")
            self.save()
            return f"Withdrawal of ${amount} successful. New balance: ${self.balance}"
        elif amount <= 0:
            return "Invalid withdrawal amount. Please enter a positive value."
        else:
            return "Insufficient funds for withdrawal."

    def display_balance(self):
        return f"Current balance for {self.username}'s account ({self.account_number}): ${self.balance}"

    def display_transactions(self):
        return f"Transaction history for {self.username}'s account ({self.account_number}):\n{', '.join(self.transactions)}"
