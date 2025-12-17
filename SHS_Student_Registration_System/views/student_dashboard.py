from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, \
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QScrollArea, QComboBox, QDateEdit, QFileDialog
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QRect, QDate
import os


class StudentDashboard(QWidget):
    def __init__(self, main_window, controller):
        super().__init__()
        self.main_window = main_window
        self.controller = controller
        self.setWindowTitle("SHS Registration System")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background-color:rgb(50, 50, 50);")

        layout = QVBoxLayout()

        # --- LOGO ---
        self.logo = QLabel(self)
        pixmap = QPixmap(
            "D:\\Applications\\Productivity\\PyCharm\\Projects\\IT5 Final Project\\IT5_SHS_Registration_System\\files\\Final Logo - White.png")
        pixmap = pixmap.scaled(150, 45, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setGeometry(525, 25, 150, 45)

        # --- MAIN SHAPE ---
        self.shape_main = QWidget(self)
        self.shape_main.setGeometry(300, 100, 600, 600)
        self.shape_main.setStyleSheet(
            "background-color: rgb(60, 60, 60);"
            "border-radius: 0px;"
            "border: 1px solid rgba(200, 0, 0, 50);"
        )

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(10)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.shape_main.setGraphicsEffect(shadow)

        # Header bar
        self.shape_header = QWidget(self)
        self.shape_header.setGeometry(400, 75, 400, 50)
        self.shape_header.setStyleSheet(
            "background-color: rgb(100, 0, 0);"
            "border-radius: 0px;"
            "border: 1px solid rgb(50, 50, 50);"
        )

        self.header = QLabel("STUDENT DASHBOARD", self)
        self.header.setGeometry(425, 85, 350, 30)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 20px;
                font-weight: bold;
            }
        """)

        # --- TEXT FIELDS ---
        # LRN
        self.lrn = QLabel("LRN", self)
        self.lrn.setGeometry(450, 175, 300, 25)
        self.lrn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lrn.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 16px;
                font-weight: normal;
            }
        """)

        # NAME
        self.fullname = QLabel("NAME", self)
        self.fullname.setGeometry(325, 225, 550, 50)
        self.fullname.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fullname.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 30px;
                font-weight: normal;
            }
        """)

        # School Year
        self.school_year = QLabel("School Year", self)
        self.school_year.setGeometry(450, 300, 300, 25)
        self.school_year.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.school_year.setStyleSheet(self.lrn.styleSheet())

        # Grade Level
        self.grade_level = QLabel("Grade Level", self)
        self.grade_level.setGeometry(450, 350, 300, 25)
        self.grade_level.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grade_level.setStyleSheet(self.lrn.styleSheet())

        # Track - Strand
        self.track_strand = QLabel("TRACK - STRAND", self)
        self.track_strand.setGeometry(450, 400, 300, 25)
        self.track_strand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.track_strand.setStyleSheet(self.lrn.styleSheet())

        # STATUS field
        self.status1 = QLineEdit(self)
        self.status1.setGeometry(450, 455, 300, 30)
        self.status1.setReadOnly(True)
        self.status1.setEnabled(False)
        self.status1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status1.setText("Pending")
        self.status1.setStyleSheet("""
            QLineEdit {
                background-color: rgb(200, 200, 0);
                border-radius: 0px;
                border: none;
                padding: 4px 8px;
                color: rgb(50, 50, 50);
                font-family: Poppins;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        # View Registration Summary button
        self.summary = QPushButton(self)
        self.summary.setText("View Registration Summary")
        self.summary.setGeometry(450, 530, 300, 30)
        self.summary.setStyleSheet("""
            QPushButton {
                background-color: rgba(60, 60, 60, 0);
                color: rgb(193, 193, 193);
                border-radius: 0px;
                border: 1px solid rgb(193, 193, 193);
                padding: 4px 8px;
                font-family: Poppins;
                font-size: 14px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: rgb(70, 70, 70);
            }
            QPushButton:pressed {
                background-color: rgb(40, 40, 40);
            }
        """)

        # Logout button
        self.logout = QPushButton(self)
        self.logout.setText("LOGOUT")
        self.logout.setGeometry(1050, 25, 125, 30)
        self.logout.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: rgb(234, 234, 234);
                border-radius: 0px;
                border: 1px solid rgba(0, 0, 0, 0);
                padding: 2px 6px;
                font-family: Poppins;
                font-size: 16px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 40);
            }
        """)

        # Connect buttons
        self.summary.clicked.connect(self.handle_view_summary)
        self.logout.clicked.connect(self.handle_logout)

        self.setLayout(layout)

    def load_student_data(self, account_id):
        """Load and display student data"""
        student = self.controller.get_student_by_account_id(account_id)
        if not student:
            return
        
        # Update LRN
        lrn = student.get("LRN") or "N/A"
        self.lrn.setText(lrn)

        # Update Full Name
        first_name = student.get("FirstName") or ""
        middle_name = student.get("MiddleName") or ""
        last_name = student.get("LastName") or ""
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        if not full_name:
            full_name = "N/A"
        self.fullname.setText(full_name)

        # Update School Year and Grade Level
        # Get school year from registration records (most recent)
        student_id = student.get("StudentID")
        school_year = "N/A"
        grade_level = student.get("GradeLevel") or "N/A"
        registrations = None
        
        if student_id:
            registrations = self.controller.get_student_dashboard(student_id)
            if registrations and len(registrations) > 0:
                # Get the most recent registration for school year
                latest_reg = registrations[0]
                school_year = latest_reg.get("SchoolYear") or "N/A"
                # Also get grade level from registration if available
                if latest_reg.get("GradeLevel"):
                    grade_level = latest_reg.get("GradeLevel")
        
        self.school_year.setText(str(school_year))
        self.grade_level.setText(str(grade_level))

        # Update Track & Strand
        track = student.get("Track") or ""
        strand = student.get("Strand") or ""
        if track and strand:
            track_strand = f"{track} - {strand}"
        elif track:
            track_strand = track
        elif strand:
            track_strand = strand
        else:
            track_strand = "N/A"
        self.track_strand.setText(track_strand)

        # Get registration status
        if student_id:
            if registrations is None:
                registrations = self.controller.get_student_dashboard(student_id)
            if registrations and len(registrations) > 0:
                # Get the most recent registration
                latest_reg = registrations[0]
                status = latest_reg.get("Status", "Pending")
                self.status1.setText(status)

                # Update status color based on status
                if status == "Approved":
                    self.status1.setStyleSheet("""
                        QLineEdit {
                            background-color: rgb(0, 180, 0);
                            border-radius: 0px;
                            border: none;
                            padding: 4px 8px;
                            color: rgb(50, 50, 50);
                            font-family: Poppins;
                            font-size: 16px;
                            font-weight: bold;
                        }""")
                elif status == "Rejected":
                    self.status1.setStyleSheet("""
                        QLineEdit {
                            background-color: rgb(180, 0, 0);
                            border-radius: 0px;
                            border: none;
                            padding: 4px 8px;
                            color: rgb(50, 50, 50);
                            font-family: Poppins;
                            font-size: 16px;
                            font-weight: bold;
                        }""")
                else:
                    self.status1.setStyleSheet("""
                        QLineEdit {
                            background-color: rgb(200, 200, 0);
                            border-radius: 0px;
                            border: none;
                            padding: 4px 8px;
                            color: rgb(50, 50, 50);
                            font-family: Poppins;
                            font-size: 16px;
                            font-weight: bold;
                        }""")
            else:
                self.status1.setText("No Registration")
        else:
            self.status1.setText("N/A")

    def handle_view_summary(self):
        """Handle view summary button click"""
        # Get student ID from current user
        if self.main_window.current_user:
            account_id = self.main_window.current_user.get("account_id")
            student = self.controller.get_student_by_account_id(account_id)
            if student and student.get("StudentID"):
                # Load summary data if method exists
                if hasattr(self.main_window.views["student_summary"], "load_summary_data"):
                    self.main_window.views["student_summary"].load_summary_data(student.get("StudentID"))
                self.main_window.switch_view("student_summary")

    def handle_logout(self):
        """Handle logout button click"""
        self.main_window.current_user = None
        self.main_window.switch_view("login")
