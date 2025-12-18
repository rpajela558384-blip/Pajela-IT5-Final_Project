# controllers/admin_controller.py

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from models.student_model import StudentModel
from models.registration_model import RegistrationModel
from models.account_model import AccountModel
from models.employee_model import EmployeeModel

class AdminController:
    def __init__(self, connection_params):
        self.student_model = StudentModel(connection_params)
        self.registration_model = RegistrationModel(connection_params)
        self.account_model = AccountModel(connection_params)
        self.employee_model = EmployeeModel(connection_params)

    def get_all_students(self):
        conn = self.student_model.create_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM students"
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students

    def get_all_registrations(self):
        conn = self.registration_model.create_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT rr.*, 
                   e.FullName as ValidatorName,
                   rr.ValidatedBy as ValidatorID
            FROM registration_record rr
            LEFT JOIN employee e ON rr.ValidatedBy = e.EmployeeID
            ORDER BY rr.SubmittedAt DESC
        """
        cursor.execute(query)
        registrations = cursor.fetchall()
        cursor.close()
        conn.close()
        return registrations

    def generate_registration_summary(self):
        records = self.get_all_registrations()
        if not records:
            return pd.DataFrame()
        df = pd.DataFrame(records)
        summary = df.groupby('Status').size().reset_index(name='Count')
        return summary

    def export_summary_to_csv(self, filepath):
        summary = self.generate_registration_summary()
        if not summary.empty:
            summary.to_csv(filepath, index=False)
            return True
        return False

    def get_all_accounts(self):
        """Get all accounts with UUID (StudentID or EmployeeID)"""
        conn = self.account_model.create_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT a.*,
                   COALESCE(s.StudentID, e.EmployeeID) as UUID
            FROM accounts a
            LEFT JOIN students s ON a.AccountID = s.AccountID
            LEFT JOIN employee e ON a.AccountID = e.AccountID
            ORDER BY a.AccountID
        """
        cursor.execute(query)
        accounts = cursor.fetchall()
        cursor.close()
        conn.close()
        return accounts

    def create_account(self, username, password, role, security_question=None, security_answer=None):
        """Create a new account and automatically create employee record for admin/registrar roles"""
        # Create the account first
        account_id = self.account_model.create_account(username, password, role, security_question, security_answer)
        
        if account_id and role in ["admin", "registrar"]:
            # Automatically create employee record for admin/registrar accounts
            employee_id = self.employee_model.generate_employee_id()
            if employee_id:
                # Create employee record with the account_id
                success = self.employee_model.create_employee(employee_id, account_id, username)
                if success:
                    print(f"Created employee record {employee_id} for account {account_id}")
                else:
                    print(f"Warning: Failed to create employee record for account {account_id}")
        
        return account_id

    def update_account(self, account_id, username=None, password=None, role=None, security_question=None, security_answer=None):
        """Update an account"""
        return self.account_model.update_account(account_id, username, password, role, security_question, security_answer)

    def get_account_by_id(self, account_id):
        """Get account by ID"""
        return self.account_model.get_account_by_id(account_id)

    def get_monthly_registrations(self, year=None):
        """Get monthly registration data"""
        return self.registration_model.get_monthly_registrations(year)

    def is_student_account(self, account_id):
        """Check if account belongs to a student"""
        account = self.account_model.get_account_by_id(account_id)
        if account and account.get("Role") == "student":
            return True
        return False
