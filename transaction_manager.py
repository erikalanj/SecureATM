from encryption import encrypt_aes, decrypt_aes
from helpers import is_valid_number
from datetime import datetime
from Crypto.Random import get_random_bytes
from constants import TRANSACTION_FILE


class TransactionManager:
    def __init__(self, aes_key):
        self.aes_key = aes_key  # Store the AES encryption key

    # Handles deposit transactions
    def deposit(self, username, amount):
        if not is_valid_number(amount):  # Validate that the amount is numeric
            print("Error: Amount must be a number.")
            return
        if amount <= 0:
            print("Error: Deposit amount must be greater than zero.")
            return
        iv = get_random_bytes(
            16
        )  # Generate a random 16-byte initialization vector (IV)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        encrypted_data = encrypt_aes(
            f"{username}|deposit|{amount}|{timestamp}", self.aes_key, iv
        )
        # Append encrypted transaction data to the transaction file
        with open(TRANSACTION_FILE, "a") as file:
            file.write(encrypted_data + "\n")
        print(f"Deposited {amount} into {username}'s account.")

    # Handles withdrawal transactions
    def withdraw(self, username, amount):
        if not is_valid_number(amount):
            print("Error: Amount must be a number.")
            return
        if amount <= 0:
            print("Error: Withdrawal amount must be greater than zero.")
            return
        balance = self.check_balance(username)
        if amount > balance:
            print("Error: Insufficient funds.")
            return
        iv = get_random_bytes(16)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        encrypted_data = encrypt_aes(
            f"{username}|withdrawal|{amount}|{timestamp}", self.aes_key, iv
        )
        # Append encrypted transaction data to the transaction file
        with open(TRANSACTION_FILE, "a") as file:
            file.write(encrypted_data + "\n")
        print(f"Withdrew {amount} from {username}'s account.")

    # Calculates the current balance of a user by processing their transaction history
    def check_balance(self, username):
        balance = 0  # Initialize balance
        try:
            with open(TRANSACTION_FILE, "r") as file:
                for line in file:
                    encrypted_data = line.strip()  # Read encrypted transaction data
                    decrypted_data = decrypt_aes(
                        encrypted_data, self.aes_key
                    )  # Decrypt the data
                    transaction_info = decrypted_data.split(
                        "|"
                    )  # Parse the transaction details
                    if (
                        transaction_info[0] == username
                    ):  # Check if the transaction belongs to the user
                        if transaction_info[1] == "deposit":  # Add deposit amounts
                            balance += float(transaction_info[2])
                        elif (
                            transaction_info[1] == "withdrawal"
                        ):  # Subtract withdrawal amounts
                            balance -= float(transaction_info[2])
        except (
            FileNotFoundError
        ):  # Handle case where the transaction file does not exist
            print("No transactions found.")
        return balance  # Return the calculated balance

    # Retrieves the transaction history of a user
    def get_transaction_history(self, username):
        history = []
        try:
            with open(TRANSACTION_FILE, "r") as file:
                for line in file:
                    encrypted_data = line.strip()
                    decrypted_data = decrypt_aes(encrypted_data, self.aes_key)
                    transaction_info = decrypted_data.split("|")
                    if transaction_info[0] == username:
                        history.append(transaction_info)
        except FileNotFoundError:
            print("No transactions found.")
        return history
