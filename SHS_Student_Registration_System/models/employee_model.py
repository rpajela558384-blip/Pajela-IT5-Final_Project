# models/employee_model.py

import mysql.connector
from mysql.connector import Error
from database.connect_database import get_connection_params

class EmployeeModel:
    def __init__(self, connection_params):
        self.conn_params = connection_params

    def create_connection(self):
        try:
            conn = mysql.connector.connect(**self.conn_params)
            return conn
        except Error as e:
            print(f"Database connection error: {e}")
            return None

    def generate_employee_id(self):
        """Generates a simple EmployeeID with prefix E (E1, E2, etc.)"""
        conn = self.create_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        query = "SELECT EmployeeID FROM employee WHERE EmployeeID LIKE 'E%' ORDER BY CAST(SUBSTRING(EmployeeID,2) AS UNSIGNED) DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            num = int(result[0][1:]) + 1
        else:
            num = 1
        return f"E{num}"

    def get_employee_by_account(self, account_id):
        """Fetch employee details by AccountID (used for registrar dashboard and validation)"""
        conn = self.create_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        # Explicitly select EmployeeID to ensure we get the correct field
        query = "SELECT EmployeeID, AccountID, FullName, ContactNum, Email FROM employee WHERE AccountID = %s"
        cursor.execute(query, (account_id,))
        employee = cursor.fetchone()
        cursor.close()
        conn.close()
        if employee:
            print(f"DEBUG: Retrieved employee - EmployeeID: {employee.get('EmployeeID')}, FullName: {employee.get('FullName')}")
        return employee

    def create_employee(self, employee_id, account_id, full_name=None, contact_num=None, email=None):
        """Create a new employee record"""
        conn = self.create_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        query = """
            INSERT INTO employee (EmployeeID, AccountID, FullName, ContactNum, Email)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            print(f"DEBUG: Creating employee record - EmployeeID: {employee_id}, AccountID: {account_id}, FullName: {full_name}")
            cursor.execute(query, (employee_id, account_id, full_name, contact_num, email))
            conn.commit()
            print(f"DEBUG: Successfully created employee record with EmployeeID: {employee_id}")
            return True
        except Error as e:
            print(f"Error creating employee: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
