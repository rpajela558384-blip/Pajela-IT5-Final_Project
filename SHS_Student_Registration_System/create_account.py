# create_account.py
# Purpose: Console-based script for creating demo accounts. Provides a simple command-line interface
# for creating accounts with different roles (student, registrar, admin). This demonstrates OOP by
# using the AccountModel class to handle database operations.

from database.connect_database import get_connection_params
from models.account_model import AccountModel

# Main function: Console-based account creation script
def main():
    connection_params = get_connection_params()
    account_model = AccountModel(connection_params)

    print("=== Create a Demo Account ===")

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    role = input("Enter role (student/registrar/admin): ").strip().lower()

    security_question = input("Enter security question (optional): ").strip()
    security_answer = input("Enter security answer (optional): ").strip()

    account_id = account_model.create_account(
        username=username,
        password=password,
        role=role,
        security_question=security_question if security_question else None,
        security_answer=security_answer if security_answer else None
    )

    if account_id:
        print(f"Account created successfully! AccountID: {account_id}")
    else:
        print("Failed to create account. Check the logs for errors.")

if __name__ == "__main__":
    main()
