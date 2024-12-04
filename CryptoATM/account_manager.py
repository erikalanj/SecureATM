from encryption import encrypt_aes, decrypt_aes, hash_password
from helpers import is_valid_date, is_valid_password
from base64 import b64decode
from datetime import datetime
from Crypto.Random import get_random_bytes
from constants import ACCOUNT_FILE
import os
from hashlib import sha256
from secrets import choice
import string


class AccountManager:
    def __init__(self, aes_key):
        self.aes_key = aes_key

    def generate_salt(self):
        # Generate a 16-byte random salt
        return os.urandom(16)

    def hash_password_with_salt(self, password, salt):
        # Combine password and salt, then hash them together
        return sha256(salt + password.encode()).hexdigest()

    def suggest_strong_password(self):
        # Generate a strong password with at least 12 characters
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = "".join(choice(alphabet) for _ in range(16))
        return password

    def create_account(self, username, dob, password):
        if not is_valid_date(dob):
            print("Error: Invalid date of birth. Use format dd/mm/yyyy.")
            return

        if not is_valid_password(password):
            print(
                "Error: Password must be at least 8 characters long, include a number, and a special character."
            )
            # Suggest a secure password if the provided one is weak
            suggested_password = self.suggest_strong_password()
            print(f"Suggestion: Use this strong password: {suggested_password}")
            return

        iv = get_random_bytes(16)
        salt = self.generate_salt()
        salted_hashed_password = self.hash_password_with_salt(password, salt)

        encrypted_data = encrypt_aes(
            f"{username}|{dob}|{salt.hex()}|{salted_hashed_password}", self.aes_key, iv
        )

        with open(ACCOUNT_FILE, "a") as file:
            file.write(encrypted_data + "\n")

        print("Account created successfully!")

    def authenticate(self, username, password):
        try:
            with open(ACCOUNT_FILE, "r") as file:
                for line in file:
                    encrypted_data = line.strip()
                    decrypted_data = decrypt_aes(encrypted_data, self.aes_key)
                    user_info = decrypted_data.split("|")
                    if user_info[0] == username:
                        stored_salt = bytes.fromhex(
                            user_info[2]
                        )  # Convert hex string back to bytes
                        stored_hashed_password = user_info[3]
                        # Hash the entered password with the stored salt
                        hashed_input_password = self.hash_password_with_salt(
                            password, stored_salt
                        )
                        if hashed_input_password == stored_hashed_password:
                            print("Login successful!")
                            return True
                        else:
                            print("Error: Incorrect password.")
                            return False
            print("Error: User not found.")
        except FileNotFoundError:
            print("Error: No accounts exist yet.")
        return False

    def delete_account(self, username, password):
        # First authenticate the user
        if not self.authenticate(username, password):
            print("Account deletion failed due to authentication error.")
            return

        try:
            # Read all lines from the account file
            with open(ACCOUNT_FILE, "r") as file:
                lines = file.readlines()

            # Filter out the line that contains the account to be deleted
            with open(ACCOUNT_FILE, "w") as file:
                for line in lines:
                    encrypted_data = line.strip()
                    decrypted_data = decrypt_aes(encrypted_data, self.aes_key)
                    user_info = decrypted_data.split("|")
                    # Write back all lines except the account that matches the username
                    if user_info[0] != username:
                        file.write(line)

            print(f"Account {username} deleted successfully.")
        except FileNotFoundError:
            print("Error: Accounts file not found.")
