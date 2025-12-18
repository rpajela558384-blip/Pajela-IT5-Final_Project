# main.py
# Purpose: Entry point of the application. Initializes the PyQt6 application, sets up database connection,
# creates models and controllers, and launches the main window. Also contains utility functions for database setup.

import sys
from PyQt6.QtWidgets import QApplication
from database.connect_database import get_connection_params
from models.account_model import AccountModel
from controllers.authentication import AuthenticationController
from views.login_page import LoginWindow
from main_window import MainWindow

from database.setup_database import create_connection, create_database, create_tables
import mysql.connector

# Function to wipe/delete the entire database
def wipe_database():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="")
        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS shs_registration_system")
        conn.commit()
        cursor.close()
        conn.close()
        print("Database wiped.")
    except mysql.connector.Error as e:
        print(f"Error wiping database: {e}")

# Function to recreate the database from scratch (drops and recreates all tables)
def recreate_database():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        create_database(cursor)
        create_tables(cursor)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database recreated fresh.\n")
    except mysql.connector.Error as e:
        print(f"Error recreating database: {e}")


# Main function: Initializes the application and starts the event loop
def main():
    conn_params = get_connection_params()
    account_model = AccountModel(conn_params)

    app = QApplication(sys.argv)

    auth_ctrl = AuthenticationController(account_model)
    main_win = MainWindow(conn_params)
    main_win.show()

    # Callback function for successful login (currently just prints, routing handled in MainWindow)
    def on_login_success(user):
        print(f"Logged in as {user['role']} (AccountID: {user['account_id']})")

    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    # wipe_database()
    # recreate_database()
    main()
