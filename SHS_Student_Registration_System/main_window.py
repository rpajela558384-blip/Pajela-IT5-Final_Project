# MainWindow.py

from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from database.connect_database import get_connection_params

# Import all views
from views.login_page import LoginWindow
from views.registration_form import RegistrationForm
from views.student_dashboard import StudentDashboard
from views.student_summary import StudentSummary
from views.registrar_dashboard import RegistrarDashboard
from views.registrar_validation import RegistrarValidation
from views.admin_dashboard import AdminDashboard
from views.account_recovery import AccountRecovery
from views.account_recovery_security import AccountRecoverySecurity
from views.account_recovery_reset import AccountRecoveryReset

# Import controllers
from controllers.authentication import AuthenticationController
from controllers.student_controller import StudentController
from controllers.registrar_controller import RegistrarController
from controllers.admin_controller import AdminController

# Import models
from models.registration_model import RegistrationModel
from models.account_model import AccountModel
from models.student_model import StudentModel

class MainWindow(QMainWindow):
    def __init__(self, connection_params):
        super().__init__()
        self.setWindowTitle("SHS Student Registration System")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background-color:rgb(50, 50, 50);")

        # Initialize models
        self.account_model = AccountModel(connection_params)
        self.student_model = StudentModel(connection_params)
        self.registration_model = RegistrationModel(connection_params)

        # Store connection params
        self.connection_params = connection_params

        # Initialize controllers
        self.auth_controller = AuthenticationController(self.account_model)
        self.student_controller = StudentController(self.student_model, self.registration_model)
        self.registrar_controller = RegistrarController(connection_params)
        self.admin_controller = AdminController(connection_params)

        # Create stacked widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize views
        self.views = {}
        self.current_user = None  # Store current logged-in user info
        self.recovery_account_id = None  # Store account ID during recovery process
        self.selected_registration_id = None  # Store selected registration ID for validation
        self.init_views()

    def init_views(self):
        """Initialize all views and add them to the stacked widget"""

        # Login
        self.views["login"] = LoginWindow(self, self.auth_controller, on_login_success=self.handle_login_success)
        self.stack.addWidget(self.views["login"])

        # MainWindow.py
        self.views["registration"] = RegistrationForm(
            main_window=self,
            controller=self.student_controller,  # for student creation
            auth_controller=self.auth_controller  # for account creation
        )
        self.stack.addWidget(self.views["registration"])

        # Student Dashboard
        self.views["student_dashboard"] = StudentDashboard(self, self.student_controller)
        self.stack.addWidget(self.views["student_dashboard"])

        # Student Summary
        self.views["student_summary"] = StudentSummary(self, self.student_controller)
        self.stack.addWidget(self.views["student_summary"])

        # Registrar Dashboard
        self.views["registrar_dashboard"] = RegistrarDashboard(self, self.registrar_controller)
        self.stack.addWidget(self.views["registrar_dashboard"])

        # Registrar Validation
        self.views["registrar_validation"] = RegistrarValidation(self, self.registrar_controller)
        self.stack.addWidget(self.views["registrar_validation"])

        # Admin Dashboard
        self.views["admin_dashboard"] = AdminDashboard(self, self.admin_controller)
        self.stack.addWidget(self.views["admin_dashboard"])

        # Account Recovery
        self.views["account_recovery"] = AccountRecovery(self, self.auth_controller)
        self.stack.addWidget(self.views["account_recovery"])

        # Account Recovery Security
        self.views["account_recovery_security"] = AccountRecoverySecurity(self, self.auth_controller)
        self.stack.addWidget(self.views["account_recovery_security"])
        # Load security question when view is shown
        if hasattr(self.views["account_recovery_security"], "load_security_question"):
            # call this when switching to the view
            pass

        # Account Recovery Reset
        self.views["account_recovery_reset"] = AccountRecoveryReset(self, self.auth_controller)
        self.stack.addWidget(self.views["account_recovery_reset"])

        # Set initial view
        self.stack.setCurrentWidget(self.views["login"])

    def switch_view(self, view_name):
        """Switch to a different view in the stacked widget"""
        if view_name in self.views:
            self.stack.setCurrentWidget(self.views[view_name])
            # Load security question when switching to account_recovery_security
            if view_name == "account_recovery_security":
                if hasattr(self.views[view_name], "load_security_question"):
                    self.views[view_name].load_security_question()
            # Refresh registrar dashboard when switching to it
            elif view_name == "registrar_dashboard":
                if hasattr(self.views[view_name], "load_registration_records"):
                    self.views[view_name].load_registration_records()
            # Refresh admin dashboard statistics when switching to it
            elif view_name == "admin_dashboard":
                if hasattr(self.views[view_name], "load_statistics"):
                    self.views[view_name].load_statistics()
            # Load registration data when switching to registrar_validation
            elif view_name == "registrar_validation":
                if hasattr(self, "selected_registration_id") and self.selected_registration_id:
                    if hasattr(self.views[view_name], "load_registration_data"):
                        self.views[view_name].load_registration_data(self.selected_registration_id)

    def handle_login_success(self, user):
        """Handle successful login and route to appropriate dashboard"""
        role = user.get("role")
        account_id = user.get("account_id")
        
        # Store current user info
        self.current_user = user
        
        if role == "student":
            # Update student dashboard with user data
            if hasattr(self.views["student_dashboard"], "load_student_data"):
                self.views["student_dashboard"].load_student_data(account_id)
            self.switch_view("student_dashboard")
        elif role == "registrar":
            self.switch_view("registrar_dashboard")
        elif role == "admin":
            self.switch_view("admin_dashboard")
        else:
            # Unknown role, stay on login
            pass
