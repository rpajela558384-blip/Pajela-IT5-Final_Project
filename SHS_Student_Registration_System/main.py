import sys
from PyQt6.QtWidgets import QApplication
from database.connect_database import get_connection_params
from models.account_model import AccountModel
from controllers.authentication import AuthenticationController
from views.login_page import LoginWindow
from main_window import MainWindow

from database.setup_database import create_connection, create_database, create_tables
import mysql.connector

# --- DATABASE SETUP FUNCTIONS ---
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


def main():
    conn_params = get_connection_params()
    account_model = AccountModel(conn_params)

    app = QApplication(sys.argv)

    auth_ctrl = AuthenticationController(account_model)
    main_win = MainWindow(conn_params)
    main_win.show()

    def on_login_success(user):
        print(f"Logged in as {user['role']} (AccountID: {user['account_id']})")
        # TODO: Open corresponding dashboard window

    sys.exit(app.exec())


if __name__ == "__main__":
    # wipe_database()
    # recreate_database()
    main()
