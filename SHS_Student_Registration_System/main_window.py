# main_window.py
# Purpose: Main application window that manages all views using a QStackedWidget. This follows the OOP pattern
# by encapsulating view management, user state, and navigation logic in a single class. It initializes all
# models, controllers, and views, and handles switching between different UI screens based on user actions.

from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from database.connect_database import get_connection_params

# Import all view classes (UI windows)
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

# Import controller classes (business logic handlers)
from controllers.authentication import AuthenticationController
from controllers.student_controller import StudentController
from controllers.registrar_controller import RegistrarController
from controllers.admin_controller import AdminController

# Import model classes (database interaction layer)
from models.registration_model import RegistrationModel
from models.account_model import AccountModel
from models.student_model import StudentModel

# MainWindow class - OOP: Encapsulates all application state and view management
# This is an OOP class because it groups related data (views, models, controllers, user state) and
# methods (view switching, initialization) into a single cohesive unit, following encapsulation principles.
class MainWindow(QMainWindow):
    def __init__(self, connection_params):
        super().__init__()
        self.setWindowTitle("SHS Student Registration System")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background-color:rgb(50, 50, 50);")

        # Initialize model instances (OOP: Models handle database operations)
        self.account_model = AccountModel(connection_params)
        self.student_model = StudentModel(connection_params)
        self.registration_model = RegistrationModel(connection_params)

        # Store connection parameters for later use
        self.connection_params = connection_params

        # Initialize controller instances (OOP: Controllers handle business logic and coordinate between models and views)
        self.auth_controller = AuthenticationController(self.account_model)
        self.student_controller = StudentController(self.student_model, self.registration_model)
        self.registrar_controller = RegistrarController(connection_params)
        self.admin_controller = AdminController(connection_params)

        # Create stacked widget to manage multiple views (only one visible at a time)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Dictionary to store all view instances
        self.views = {}
        # Store current logged-in user information (account_id, role, etc.)
        self.current_user = None
        # Store account ID during password recovery process
        self.recovery_account_id = None
        # Store selected registration ID when navigating to validation view
        self.selected_registration_id = None
        self.init_views()

    # Initialize all view widgets and add them to the stacked widget
    def init_views(self):
        # Login view - initial screen for user authentication
        self.views["login"] = LoginWindow(self, self.auth_controller, on_login_success=self.handle_login_success)
        self.stack.addWidget(self.views["login"])

        # Registration form view - multi-page form for new student registration
        self.views["registration"] = RegistrationForm(
            main_window=self,
            controller=self.student_controller,  # for student creation
            auth_controller=self.auth_controller  # for account creation
        )
        self.stack.addWidget(self.views["registration"])

        # Student dashboard view - displays student information and registration status
        self.views["student_dashboard"] = StudentDashboard(self, self.student_controller)
        self.stack.addWidget(self.views["student_dashboard"])

        # Student summary view - shows detailed registration information
        self.views["student_summary"] = StudentSummary(self, self.student_controller)
        self.stack.addWidget(self.views["student_summary"])

        # Registrar dashboard view - shows list of pending registrations for validation
        self.views["registrar_dashboard"] = RegistrarDashboard(self, self.registrar_controller)
        self.stack.addWidget(self.views["registrar_dashboard"])

        # Registrar validation view - detailed view for validating a specific registration
        self.views["registrar_validation"] = RegistrarValidation(self, self.registrar_controller)
        self.stack.addWidget(self.views["registrar_validation"])

        # Admin dashboard view - administrative interface for managing accounts
        self.views["admin_dashboard"] = AdminDashboard(self, self.admin_controller)
        self.stack.addWidget(self.views["admin_dashboard"])

        # Account recovery view - first step: enter username to recover account
        self.views["account_recovery"] = AccountRecovery(self, self.auth_controller)
        self.stack.addWidget(self.views["account_recovery"])

        # Account recovery security view - second step: answer security question
        self.views["account_recovery_security"] = AccountRecoverySecurity(self, self.auth_controller)
        self.stack.addWidget(self.views["account_recovery_security"])

        # Account recovery reset view - final step: set new password
        self.views["account_recovery_reset"] = AccountRecoveryReset(self, self.auth_controller)
        self.stack.addWidget(self.views["account_recovery_reset"])

        # Set the login view as the initial visible view
        self.stack.setCurrentWidget(self.views["login"])

    # Switch to a different view in the stacked widget and refresh data if needed
    def switch_view(self, view_name):
        if view_name in self.views:
            self.stack.setCurrentWidget(self.views[view_name])
            # Load security question when switching to account recovery security view
            if view_name == "account_recovery_security":
                if hasattr(self.views[view_name], "load_security_question"):
                    self.views[view_name].load_security_question()
            # Refresh registration records when switching to registrar dashboard
            elif view_name == "registrar_dashboard":
                if hasattr(self.views[view_name], "load_registration_records"):
                    self.views[view_name].load_registration_records()
            # Refresh statistics when switching to admin dashboard
            elif view_name == "admin_dashboard":
                if hasattr(self.views[view_name], "load_statistics"):
                    self.views[view_name].load_statistics()
            # Load registration data when switching to registrar validation view
            elif view_name == "registrar_validation":
                if hasattr(self, "selected_registration_id") and self.selected_registration_id:
                    if hasattr(self.views[view_name], "load_registration_data"):
                        self.views[view_name].load_registration_data(self.selected_registration_id)

    # Handle successful login and route user to appropriate dashboard based on their role
    def handle_login_success(self, user):
        role = user.get("role")
        account_id = user.get("account_id")
        
        # Store current user information for use throughout the application
        self.current_user = user
        
        # Route to appropriate dashboard based on user role
        if role == "student":
            # Load student data and switch to student dashboard
            if hasattr(self.views["student_dashboard"], "load_student_data"):
                self.views["student_dashboard"].load_student_data(account_id)
            self.switch_view("student_dashboard")
        elif role == "registrar":
            # Switch to registrar dashboard
            self.switch_view("registrar_dashboard")
        elif role == "admin":
            # Switch to admin dashboard
            self.switch_view("admin_dashboard")
        else:
            # Unknown role - stay on login page
            pass
