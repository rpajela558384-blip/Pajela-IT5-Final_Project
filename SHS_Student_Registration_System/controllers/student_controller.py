# controllers/student_controller.py

from models.student_model import StudentModel
from models.registration_model import RegistrationModel

class StudentController:
    def __init__(self, student_model, registration_model):
        # Accepts model instances instead of connection_params
        self.student_model = student_model
        self.registration_model = registration_model

    def create_student_record(self, student_data, address_data=None, academic_data=None, parent_data=None):
        """
        Creates a new student along with address, academic, and parent/guardian info.
        Returns StudentID if successful, False otherwise.
        """
        return self.student_model.create_student(
            student_data["account_id"],
            student_data.get("lrn"),
            student_data.get("first_name"),
            student_data.get("middle_name"),
            student_data.get("last_name"),
            student_data.get("gender"),
            student_data.get("birthdate"),
            student_data.get("age"),
            student_data.get("nationality"),
            student_data.get("religion"),
            student_data.get("civil_status"),
            student_data.get("contact_num"),
            student_data.get("email"),
            address_data,
            academic_data,
            parent_data
        )

    def get_student_dashboard(self, student_id):
        """
        Fetches dashboard data for a student (e.g., current registration status).
        Returns a dict with relevant info.
        """
        return self.registration_model.get_registration_by_student(student_id)

    def get_registration_summary(self, student_id):
        """
        Fetches all registration records for a student.
        Returns a list of registration dicts.
        """
        return self.registration_model.get_registration_by_student(student_id)

    def get_student_by_account_id(self, account_id):
        """Get student information by account ID"""
        return self.student_model.get_student_by_account_id(account_id)

    def get_complete_student_data(self, student_id):
        """Get complete student data including address, academic, and parent info"""
        return self.student_model.get_complete_student_data(student_id)