# controllers/registrar_controller.py

from models.employee_model import EmployeeModel
from models.registration_model import RegistrationModel

class RegistrarController:
    def __init__(self, connection_params):
        self.employee_model = EmployeeModel(connection_params)
        self.registration_model = RegistrationModel(connection_params)

    def get_registrar_info(self, account_id):
        """Fetches the employee record for the logged-in registrar."""
        return self.employee_model.get_employee_by_account(account_id)

    def get_all_registration_records(self):
        """Returns a list of all registration records with student information."""
        conn = self.registration_model.create_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT rr.*, s.LRN, s.FirstName, s.MiddleName, s.LastName
            FROM registration_record rr
            LEFT JOIN students s ON rr.StudentID = s.StudentID
            ORDER BY rr.SubmittedAt DESC
        """
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records

    def get_registration_details(self, registration_id):
        """Returns detailed info for a single registration with complete student data."""
        conn = self.registration_model.create_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT rr.*, 
                   s.*, 
                   a.GradeLevel, a.Track, a.Strand,
                   ad.HouseNum, ad.Barangay, ad.City, ad.Province, ad.ZIP,
                   pg.Name as PGName, pg.Relationship, pg.Occupation, pg.Address as PGAddress, pg.ContactNum as PGContact
            FROM registration_record rr
            LEFT JOIN students s ON rr.StudentID = s.StudentID
            LEFT JOIN academic a ON s.StudentID = a.StudentID
            LEFT JOIN address ad ON s.StudentID = ad.StudentID
            LEFT JOIN parent_guardian pg ON s.StudentID = pg.StudentID
            WHERE rr.RegistrationID = %s
        """
        cursor.execute(query, (registration_id,))
        record = cursor.fetchone()
        cursor.close()
        conn.close()
        return record
    
    def get_registration_documents(self, registration_id):
        """Get all documents for a registration."""
        conn = self.registration_model.create_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM documents WHERE RegistrationID = %s"
        cursor.execute(query, (registration_id,))
        documents = cursor.fetchall()
        cursor.close()
        conn.close()
        return documents

    def validate_registration(self, registration_id, status, account_id):
        employee_id = None
        
        if not account_id:
            print(f"ERROR: No account_id provided for validation")
            return False
        
        # Get employee ID from account ID
        employee = self.employee_model.get_employee_by_account(account_id)
        if not employee:
            print(f"ERROR: No employee record found for account {account_id}. Employee record must exist for validation.")
            return False
        
        # Debug: Print the entire employee record
        print(f"DEBUG: Employee record: {employee}")
        
        # get EmployeeID
        employee_id = employee.get("EmployeeID")
        if not employee_id:
            print(f"ERROR: Employee record found but EmployeeID is missing for account {account_id}")
            print(f"DEBUG: Available keys in employee record: {list(employee.keys())}")
            print(f"DEBUG: Full employee record: {employee}")
            return False
        
        # Ensure we're using the EmployeeID, not the username or FullName
        if not employee_id.startswith("E"):
            print(f"ERROR: EmployeeID '{employee_id}' doesn't start with 'E'. Expected format: E1, E2, etc.")
            print(f"ERROR: This employee record may have been created incorrectly. EmployeeID must start with 'E'.")
            return False
        
        # Double-check we're not accidentally using FullName or AccountID
        full_name = employee.get("FullName", "")
        if employee_id == full_name:
            print(f"ERROR: EmployeeID matches FullName '{full_name}'. This is incorrect - EmployeeID should be 'E1', 'E2', etc.")
            return False
        
        print(f"Validating registration {registration_id} with status {status} by employee {employee_id} (EmployeeID)")
        
        # Update the registration with the EmployeeID in ValidatedBy field
        result = self.registration_model.update_status(registration_id, status, employee_id)
        if result:
            print(f"Successfully updated registration {registration_id} with ValidatedBy={employee_id}")
            # Verify what was actually stored
            conn = self.registration_model.create_connection()
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT ValidatedBy FROM registration_record WHERE RegistrationID = %s", (registration_id,))
                result_check = cursor.fetchone()
                if result_check:
                    print(f"DEBUG: Verified ValidatedBy in database: {result_check.get('ValidatedBy')}")
                cursor.close()
                conn.close()
        else:
            print(f"Failed to update registration {registration_id}")
        return result
