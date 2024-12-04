from account_manager import AccountManager
from transaction_manager import TransactionManager
from Crypto.Random import get_random_bytes


# Main function containing the program's interactive menu
def main():
    aes_key = get_random_bytes(32)
    account_manager = AccountManager(aes_key)
    transaction_manager = TransactionManager(aes_key)

    logged_in_user = None  # Tracks the currently logged-in user

    while True:
        # Display menu options
        print(
            "1. Create Account\n2. Login\n3. Deposit\n4. Withdraw\n5. Check Balance\n6. View Transaction History\n7. Delete Account\n8. Log Out\n9. Exit"
        )
        choice = input("Enter choice: ")

        # Handle account creation
        if choice == "1":
            username = input("Enter username: ")
            dob = input("Enter DOB (dd/mm/yyyy): ")
            password = input("Enter password: ")
            account_manager.create_account(username, dob, password)

        # Handle login
        elif choice == "2":
            if logged_in_user:
                print(
                    f"Already logged in as {logged_in_user}. Please log out to switch users."
                )
                continue

            username = input("Enter username: ")
            password = input("Enter password: ")
            if account_manager.authenticate(username, password):  # Verify credentials
                logged_in_user = username  # Set logged-in user
                print(f"Welcome, {username}!")

        # Handle deposits
        elif choice == "3":
            if not logged_in_user:  # Ensure the user is logged in
                print("Please log in first to deposit.")
                continue

            username = logged_in_user
            try:
                amount = float(input("Enter amount to deposit: "))  # Validate amount
                transaction_manager.deposit(username, amount)
            except ValueError:
                print("Error: Amount must be a number.")

        # Handle withdrawals
        elif choice == "4":
            if not logged_in_user:
                print("Please log in first to withdraw.")
                continue

            username = logged_in_user
            try:
                amount = float(input("Enter amount to withdraw: "))
                transaction_manager.withdraw(username, amount)
            except ValueError:
                print("Error: Amount must be a number.")

        # Handle balance checking
        elif choice == "5":
            if not logged_in_user:
                print("Please log in first to check balance.")
                continue

            username = logged_in_user
            balance = transaction_manager.check_balance(
                username
            )  # Retrieve current balance
            print(f"Current balance for {username}: {balance}")

        # Handle transaction history viewing
        elif choice == "6":
            if not logged_in_user:
                print("Please log in first to view transaction history.")
                continue

            username = logged_in_user
            history = transaction_manager.get_transaction_history(
                username
            )  # Fetch transaction history
            if not history:
                print("No transaction history available.")
            else:
                print("Transaction History:")
                for transaction in history:  # Display each transaction
                    print(f"{transaction[1]}: {transaction[2]} on {transaction[3]}")

        # Handle account deletion
        elif choice == "7":
            if not logged_in_user:
                print("Please log in first to delete your account.")
                continue

            username = logged_in_user
            password = input("Enter password to confirm account deletion: ")
            account_manager.delete_account(username, password)  # Delete the account
            logged_in_user = None  # Log the user out after deletion

        # Handle logout
        elif choice == "8":
            if not logged_in_user:
                print("No user is logged in.")
            else:
                print(f"Logging out {logged_in_user}...")
                logged_in_user = None

        # Exit the program
        elif choice == "9":
            print("Exiting...")
            break

        # Handle invalid menu choices
        else:
            print("Invalid choice, please try again.")


# Entry point of the program
if __name__ == "__main__":
    main()
