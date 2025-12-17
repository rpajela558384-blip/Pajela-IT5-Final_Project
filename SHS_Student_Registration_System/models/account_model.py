# models/account_model.py

import mysql.connector
from mysql.connector import Error
from database.connect_database import get_connection_params
import uuid


class AccountModel:
    def __init__(self, connection_params):
        """
        connection_params: dict with keys host, user, password, database
        """
        self.conn_params = connection_params

    def create_connection(self):
        try:
            conn = mysql.connector.connect(**self.conn_params)
            return conn
        except Error as e:
            print(f"Database connection error: {e}")
            return None

    def generate_account_id(self):
        """Generates a simple AccountID with prefix A (A1, A2, etc.)"""
        conn = self.create_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        query = "SELECT AccountID FROM accounts WHERE AccountID LIKE 'A%' ORDER BY CAST(SUBSTRING(AccountID,2) AS UNSIGNED) DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            num = int(result[0][1:]) + 1
        else:
            num = 1
        return f"A{num}"

    def get_account_by_username(self, username):
        conn = self.create_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM accounts WHERE Username = %s"
        cursor.execute(query, (username,))
        account = cursor.fetchone()
        cursor.close()
        conn.close()
        return account

    def get_account_by_id(self, account_id):
        conn = self.create_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM accounts WHERE AccountID = %s"
        cursor.execute(query, (account_id,))
        account = cursor.fetchone()
        cursor.close()
        conn.close()
        return account

    def create_account(self, username, password, role, security_question=None, security_answer=None):
        conn = self.create_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        account_id = self.generate_account_id()
        query = """
            INSERT INTO accounts (AccountID, Username, Password, Role, SecurityQuestion, SecurityAnswer)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (account_id, username, password, role, security_question, security_answer))
            conn.commit()
            return account_id
        except Error as e:
            print(f"Error creating account: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update_password(self, account_id, new_password):
        conn = self.create_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        query = "UPDATE accounts SET Password = %s WHERE AccountID = %s"
        try:
            cursor.execute(query, (new_password, account_id))
            conn.commit()
            return True
        except Error as e:
            print(f"Error updating password: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def verify_security_answer(self, account_id, answer):
        conn = self.create_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        query = "SELECT SecurityAnswer FROM accounts WHERE AccountID = %s"
        cursor.execute(query, (account_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result and result[0] == answer:
            return True
        return False

    def get_all_accounts(self):
        """Get all accounts from the database"""
        conn = self.create_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM accounts ORDER BY AccountID"
        cursor.execute(query)
        accounts = cursor.fetchall()
        cursor.close()
        conn.close()
        return accounts

    def update_account(self, account_id, username=None, password=None, role=None, security_question=None, security_answer=None):
        """Update account details"""
        conn = self.create_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        if username is not None:
            updates.append("Username = %s")
            values.append(username)
        if password is not None:
            updates.append("Password = %s")
            values.append(password)
        if role is not None:
            updates.append("Role = %s")
            values.append(role)
        if security_question is not None:
            updates.append("SecurityQuestion = %s")
            values.append(security_question)
        if security_answer is not None:
            updates.append("SecurityAnswer = %s")
            values.append(security_answer)
        
        if not updates:
            cursor.close()
            conn.close()
            return False
        
        values.append(account_id)
        query = f"UPDATE accounts SET {', '.join(updates)} WHERE AccountID = %s"
        
        try:
            cursor.execute(query, values)
            conn.commit()
            return True
        except Error as e:
            print(f"Error updating account: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
