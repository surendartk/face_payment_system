from django.db import models
from datetime import datetime
import json
from decimal import Decimal

class BankAccount(models.Model):
    username = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transactions = models.TextField(default='[]')  # Store transactions as a JSON-encoded string

    def add_transaction(self, transaction_type, amount, other_account_number=None):
        transaction = {
            'type': transaction_type,
            'amount': str(amount),  # Convert Decimal to string
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'sender_account_number': self.account_number,
            'recipient_account_number': other_account_number,
        }
        current_transactions = json.loads(self.transactions)
        current_transactions.append(transaction)
        self.transactions = json.dumps(current_transactions)
        self.save()
       
    def deposit(self, amount):
        if amount > 0:
            amount = Decimal(str(amount))
            self.balance += amount
            self.add_transaction('Deposit', amount)
            return f"Deposit of ${amount} successful. New balance: ${self.balance}"
        else:
            return "Invalid deposit amount. Please enter a positive value."

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            # Ensure amount is a Decimal
            if not isinstance(amount, Decimal):
                amount = Decimal(str(amount))
            self.balance -= amount
            self.add_transaction('Withdrawal', amount)
            return f"Withdrawal of ${amount} successful. New balance: ${self.balance}"
        elif amount <= 0:
            return "Invalid withdrawal amount. Please enter a positive value."
        else:
            return "Insufficient funds for withdrawal."

    def display_balance(self):
        return f"Current balance for {self.username}'s account ({self.account_number}): ${self.balance}"

    def display_transactions(self):
    # Convert Decimal objects to string
        transactions = json.loads(self.transactions)
        formatted_transactions = [
            {
                'type': entry['type'],
                'amount': str(entry['amount']),
                'date': entry['date'],
                'sender_account_number': entry['sender_account_number'],
                'recipient_account_number': entry['recipient_account_number'],
            }
            for entry in transactions
        ]
    
        return formatted_transactions
    


class TemporaryFaceImage(models.Model):
    original_image = models.ImageField(upload_to='temporary_face_images/')
    

class UserImage(models.Model):
    username = models.CharField(max_length=255, unique=True)
    original_image = models.ImageField(upload_to='user_images/')
    facial_features = models.TextField(null=True, blank=True)

    def set_facial_features(self, features):
    # Ensure that features is a list before converting to JSON
        json_data = json.dumps(features) if isinstance(features, list) else json.dumps([features])
        self.facial_features = json_data

    def get_facial_features(self):
        return json.loads(self.facial_features) if self.facial_features else None
    