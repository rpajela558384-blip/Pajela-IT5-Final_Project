# controllers/student_controller.py
# Purpose: Controller class for student-related operations. Handles student record creation, retrieval,
# and registration management. This follows OOP by encapsulating student business logic and coordinating
# between views and models.

from models.student_model import StudentModel
from models.registration_model import RegistrationModel

# StudentController class - OOP: Encapsulates student business logic
# This is an OOP class because it groups related student operations into a cohesive unit. It uses composition
# by working with both StudentModel and RegistrationModel, demonstrating how OOP classes can collaborate
# to provide higher-level functionality.
class StudentController:
    # Constructor: Initialize controller with student and registration model instances (dependency injection)
    def __init__(self, student_model, registration_model):
        self.student_model = student_model
        self.registration_model = registration_model

    # Method: Create a new student record with related data (address, academic, parent/guardian)
    # This demonstrates OOP by providing a high-level interface that coordinates multiple model operations
    def create_student_record(self, student_data, address_data=None, academic_data=None, parent_data=None):
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

    # Method: Get student dashboard data including registration status
    def get_student_dashboard(self, student_id):
        return self.registration_model.get_registration_by_student(student_id)

    # Method: Get all registration records for a student
    def get_registration_summary(self, student_id):
        return self.registration_model.get_registration_by_student(student_id)

    # Method: Get student information by account ID
    def get_student_by_account_id(self, account_id):
        return self.student_model.get_student_by_account_id(account_id)

    # Method: Get complete student data including all related information
    def get_complete_student_data(self, student_id):
        return self.student_model.get_complete_student_data(student_id)