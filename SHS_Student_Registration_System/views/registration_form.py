from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, \
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QScrollArea, QComboBox, QDateEdit, QFileDialog
from PyQt6.QtGui import QPixmap, QColor, QValidator
from PyQt6.QtCore import Qt, QRect, QDate
import re

from controllers.authentication import AuthenticationController
from controllers.student_controller import StudentController
from models.account_model import AccountModel
from models.student_model import StudentModel
from database.connect_database import get_connection_params
import os


class RegistrationForm(QScrollArea):
    def __init__(self, main_window, controller, auth_controller):
        super().__init__()
        self.main_window = main_window
        self.controller = controller
        self.auth_controller = auth_controller  # AuthenticationController

        self.setWindowTitle("SHS Registration System")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background-color:rgb(50, 50, 50);")

        self.current_page = 1

        # --- LOGO ---
        self.logo = QLabel(self)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files", "Final Logo - White.png")
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaled(150, 45, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setGeometry(525, 25, 150, 45)

        # --- SHARED SHAPES ---
        self.shape_main = QWidget(self)
        self.shape_main.setGeometry(300, 100, 600, 600)
        self.shape_main.setStyleSheet(
            "background-color: rgb(60, 60, 60);"
            "border-radius: 0px;"
            "border: 1px solid rgba(200, 0, 0, 50);"
        )

        # Drop shadow
        main_shadow = QGraphicsDropShadowEffect()
        main_shadow.setBlurRadius(10)
        main_shadow.setXOffset(10)
        main_shadow.setYOffset(10)
        main_shadow.setColor(QColor(0, 0, 0, 150))
        self.shape_main.setGraphicsEffect(main_shadow)

        # Top header
        self.shape_header = QWidget(self)
        self.shape_header.setGeometry(400, 75, 400, 50)
        self.shape_header.setStyleSheet(
            "background-color: rgb(100, 0, 0);"
            "border-radius: 0px;"
            "border: 1px solid rgb(50, 50, 50);"
        )

        # Header label
        self.header_label = QLabel("REGISTRATION FORM", self)
        self.header_label.setGeometry(425, 85, 350, 30)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet("""
                            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                                font-family: Poppins;
                font-size: 20px;
                                font-weight: bold;
            }
        """)

        # --- COMMON STYLES ---
        self.field_label_style = """
                    QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                        font-family: Poppins;
                font-size: 12px;
                font-weight: normal;
            }
        """

        self.line_edit_style = """
                                            QLineEdit {
                                            background-color: rgb(50, 50, 50);
                border-radius: 0px;
                border: 1px solid rgb(132, 132, 132);
                padding: 6px 8px;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 12px;
                                            }
                                            QLineEdit:focus {
                border: 1px solid rgb(234, 234, 234);
                background-color: rgb(40, 40, 40);
            }
            QLineEdit:disabled {
                color: rgb(150, 150, 150);
                border: 1px solid rgba(120, 120, 120, 80);
                background-color: rgb(35, 35, 35);
            }
            QLineEdit::placeholder {
                color: rgb(150, 150, 150);
            }
        """

        self.combo_style = """
                                QComboBox {
                                    background-color: rgb(50, 50, 50);
                border-radius: 0px;
                border: 1px solid rgb(132, 132, 132);
                padding-left: 8px;
                color: rgb(234, 234, 234);
                                    font-family: Poppins;
                font-size: 12px;
                                    }
                                QComboBox::drop-down {
                width: 30px;
                border-left: 1px solid rgb(132, 132, 132);
                background-color: rgb(60, 60, 60);
                                    }
                                QComboBox QAbstractItemView {
                                    background-color: rgb(50, 50, 50);
                color: rgb(234, 234, 234);
                selection-background-color: rgb(90, 90, 90);
            }
        """

        self.date_edit_style = """
                                    QDateEdit {
                                        background-color: rgb(50, 50, 50);
                border-radius: 0px;
                border: 1px solid rgb(132, 132, 132);
                padding-left: 8px;
                color: rgb(234, 234, 234);
                                        font-family: Poppins;
                font-size: 12px;
                                        }
                                    QDateEdit::drop-down {
                                        subcontrol-origin: border;
                                        subcontrol-position: top right;
                width: 30px;
                border: 1px solid rgb(132, 132, 132);
                background-color: rgb(60, 60, 60);
            }
        """

        self.primary_button_style = """
            QPushButton {
                background-color: rgb(193, 193, 193);
                color: rgb(50, 50, 50);
                border-radius: 0px;
                border: rgb(132, 132, 132);
                padding: 6px 10px;
                font-family: Poppins;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(255, 255, 255);
            }
            QPushButton:pressed {
                background-color: rgb(175, 175, 175);
            }
            QPushButton:disabled {
                background-color: rgb(90, 90, 90);
                color: rgb(160, 160, 160);
            }
        """

        self.cancel_button_style = """
            QPushButton {
                background-color: rgba(132, 0, 0, 100);
                color: rgb(234, 234, 234);
                border-radius: 0px;
                border: 1px solid rgb(132, 132, 132);
                padding: 1px 1px;
                font-family: Poppins;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(100, 0, 0);
            }
            QPushButton:pressed {
                background-color: rgb(70, 0, 0);
            }
            QPushButton:disabled {
                background-color: rgb(90, 90, 90);
                color: rgb(160, 160, 160);
            }
        """

        # Build all pages
        self._build_page1_personal_details()
        self._build_page2_address_parent()
        self._build_page3_academic_documents()
        self._build_page4_account_credentials()

        # Setup input validation after all pages are built
        self._setup_validation()

        # Show initial page
        self._set_page(1)

    def _build_page1_personal_details(self):
        # Page title
        self.page1_title = QLabel("PERSONAL DETAILS", self)
        self.page1_title.setGeometry(450, 150, 300, 25)
        self.page1_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page1_title.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 16px;
                font-weight: normal;
            }
        """)


        self.label_lrn = QLabel("LRN", self)
        self.label_lrn.setGeometry(450, 200, 300, 20)
        self.label_lrn.setStyleSheet(self.field_label_style)

        self.input_lrn = QLineEdit(self)
        self.input_lrn.setGeometry(450, 220, 300, 30)
        self.input_lrn.setStyleSheet(self.line_edit_style)


        self.label_first_name = QLabel("First Name", self)
        self.label_first_name.setGeometry(450, 260, 300, 20)
        self.label_first_name.setStyleSheet(self.field_label_style)

        self.input_first_name = QLineEdit(self)
        self.input_first_name.setGeometry(450, 280, 300, 30)
        self.input_first_name.setStyleSheet(self.line_edit_style)


        self.label_email = QLabel("Email Address", self)
        self.label_email.setGeometry(450, 620, 300, 20)
        self.label_email.setStyleSheet(self.field_label_style)


        x_left = 450
        x_right = 625

        self.label_middle_name = QLabel("Middle Name", self)
        self.label_middle_name.setGeometry(x_left, 320, 125, 20)
        self.label_middle_name.setStyleSheet(self.field_label_style)

        self.input_middle_name = QLineEdit(self)
        self.input_middle_name.setGeometry(x_left, 340, 125, 30)
        self.input_middle_name.setStyleSheet(self.line_edit_style)

        self.label_last_name = QLabel("Last Name", self)
        self.label_last_name.setGeometry(x_right, 320, 125, 20)
        self.label_last_name.setStyleSheet(self.field_label_style)

        self.input_last_name = QLineEdit(self)
        self.input_last_name.setGeometry(x_right, 340, 125, 30)
        self.input_last_name.setStyleSheet(self.line_edit_style)

        self.label_suffix = QLabel("Suffix", self)
        self.label_suffix.setGeometry(x_left, 380, 125, 20)
        self.label_suffix.setStyleSheet(self.field_label_style)

        self.input_suffix = QLineEdit(self)
        self.input_suffix.setGeometry(x_left, 400, 125, 30)
        self.input_suffix.setStyleSheet(self.line_edit_style)

        self.label_age = QLabel("Age", self)
        self.label_age.setGeometry(x_right, 380, 125, 20)
        self.label_age.setStyleSheet(self.field_label_style)

        self.input_age = QLineEdit(self)
        self.input_age.setGeometry(x_right, 400, 125, 30)
        self.input_age.setStyleSheet(self.line_edit_style)

        self.label_gender = QLabel("Gender", self)
        self.label_gender.setGeometry(x_left, 440, 125, 20)
        self.label_gender.setStyleSheet(self.field_label_style)

        self.input_gender = QComboBox(self)
        self.input_gender.setGeometry(x_left, 460, 125, 30)
        self.input_gender.addItems(["Male", "Female"])
        self.input_gender.setStyleSheet(self.combo_style)

        self.label_birthdate = QLabel("Birthdate", self)
        self.label_birthdate.setGeometry(x_right, 440, 125, 20)
        self.label_birthdate.setStyleSheet(self.field_label_style)

        self.input_birthdate = QDateEdit(self)
        self.input_birthdate.setGeometry(x_right, 460, 125, 30)
        self.input_birthdate.setCalendarPopup(True)
        self.input_birthdate.setDate(QDate.currentDate())
        self.input_birthdate.setStyleSheet(self.date_edit_style)

        self.label_nationality = QLabel("Nationality", self)
        self.label_nationality.setGeometry(x_left, 500, 125, 20)
        self.label_nationality.setStyleSheet(self.field_label_style)

        self.input_nationality = QLineEdit(self)
        self.input_nationality.setGeometry(x_left, 520, 125, 30)
        self.input_nationality.setStyleSheet(self.line_edit_style)

        self.label_religion = QLabel("Religion", self)
        self.label_religion.setGeometry(x_right, 500, 125, 20)
        self.label_religion.setStyleSheet(self.field_label_style)

        self.input_religion = QLineEdit(self)
        self.input_religion.setGeometry(x_right, 520, 125, 30)
        self.input_religion.setStyleSheet(self.line_edit_style)

        self.label_civil_status = QLabel("Civil Status", self)
        self.label_civil_status.setGeometry(x_left, 560, 125, 20)
        self.label_civil_status.setStyleSheet(self.field_label_style)

        self.input_civil_status = QLineEdit(self)
        self.input_civil_status.setGeometry(x_left, 580, 125, 30)
        self.input_civil_status.setStyleSheet(self.line_edit_style)

        self.label_contact_number = QLabel("Contact Number", self)
        self.label_contact_number.setGeometry(x_right, 560, 125, 20)
        self.label_contact_number.setStyleSheet(self.field_label_style)

        self.input_contact_number = QLineEdit(self)
        self.input_contact_number.setGeometry(x_right, 580, 125, 30)
        self.input_contact_number.setStyleSheet(self.line_edit_style)

        self.input_email = QLineEdit(self)
        self.input_email.setGeometry(450, 640, 300, 30)
        self.input_email.setStyleSheet(self.line_edit_style)

        # Page 1: Cancel at top-left, Next at bottom-right
        self.button_cancel_1 = QPushButton("CANCEL", self)
        self.button_cancel_1.setGeometry(25, 25, 125, 30)
        self.button_cancel_1.setStyleSheet(self.cancel_button_style)

        self.button_next_1 = QPushButton("NEXT", self)
        self.button_next_1.setGeometry(775, 720, 125, 30)
        self.button_next_1.setStyleSheet(self.primary_button_style)

        self.button_cancel_1.clicked.connect(self._on_cancel_clicked)
        self.button_next_1.clicked.connect(self._on_next_clicked_page1)

    def _build_page2_address_parent(self):
        # Title
        self.page2_title_address = QLabel("ADDRESS INFORMATION", self)
        self.page2_title_address.setGeometry(450, 150, 300, 25)
        self.page2_title_address.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page2_title_address.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                        font-family: Poppins;
                font-size: 16px;
                font-weight: normal;
                    }
                """)

        # House No. / Street (long)
        self.label_house = QLabel("House No. / Street", self)
        self.label_house.setGeometry(450, 200, 300, 20)
        self.label_house.setStyleSheet(self.field_label_style)

        self.input_house = QLineEdit(self)
        self.input_house.setGeometry(450, 220, 300, 30)
        self.input_house.setStyleSheet(self.line_edit_style)

        # Barangay (left short), City / Municipality (right short)
        x_left = 450
        x_right = 625

        self.label_barangay = QLabel("Barangay", self)
        self.label_barangay.setGeometry(x_left, 260, 125, 20)
        self.label_barangay.setStyleSheet(self.field_label_style)

        self.input_barangay = QLineEdit(self)
        self.input_barangay.setGeometry(x_left, 280, 125, 30)
        self.input_barangay.setStyleSheet(self.line_edit_style)

        self.label_city = QLabel("City / Municipality", self)
        self.label_city.setGeometry(x_right, 260, 125, 20)
        self.label_city.setStyleSheet(self.field_label_style)

        self.input_city = QLineEdit(self)
        self.input_city.setGeometry(x_right, 280, 125, 30)
        self.input_city.setStyleSheet(self.line_edit_style)

        # Province (left), ZIP / Postal Code (right)
        self.label_province = QLabel("Province", self)
        self.label_province.setGeometry(x_left, 320, 125, 20)
        self.label_province.setStyleSheet(self.field_label_style)

        self.input_province = QLineEdit(self)
        self.input_province.setGeometry(x_left, 340, 125, 30)
        self.input_province.setStyleSheet(self.line_edit_style)

        self.label_zip = QLabel("ZIP / Postal Code", self)
        self.label_zip.setGeometry(x_right, 320, 125, 20)
        self.label_zip.setStyleSheet(self.field_label_style)

        self.input_zip = QLineEdit(self)
        self.input_zip.setGeometry(x_right, 340, 125, 30)
        self.input_zip.setStyleSheet(self.line_edit_style)

        # Parent / Guardian Information title
        self.page2_title_parent = QLabel("PARENT / GUARDIAN INFORMATION", self)
        self.page2_title_parent.setGeometry(450, 395, 300, 25)
        self.page2_title_parent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page2_title_parent.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                                    font-family: Poppins;
                font-size: 16px;
                font-weight: normal;
            }
        """)

        # Full Name (long)
        self.label_pg_fullname = QLabel("Full Name", self)
        self.label_pg_fullname.setGeometry(450, 430, 300, 20)
        self.label_pg_fullname.setStyleSheet(self.field_label_style)

        self.input_pg_fullname = QLineEdit(self)
        self.input_pg_fullname.setGeometry(450, 450, 300, 30)
        self.input_pg_fullname.setStyleSheet(self.line_edit_style)

        # Relationship to Student (long)
        self.label_pg_relationship = QLabel("Relationship to Student", self)
        self.label_pg_relationship.setGeometry(450, 490, 300, 20)
        self.label_pg_relationship.setStyleSheet(self.field_label_style)

        self.input_pg_relationship = QLineEdit(self)
        self.input_pg_relationship.setGeometry(450, 510, 300, 30)
        self.input_pg_relationship.setStyleSheet(self.line_edit_style)

        # Occupation (left short), Contact Number (right short)
        self.label_pg_occupation = QLabel("Occupation", self)
        self.label_pg_occupation.setGeometry(x_left, 550, 125, 20)
        self.label_pg_occupation.setStyleSheet(self.field_label_style)

        self.input_pg_occupation = QLineEdit(self)
        self.input_pg_occupation.setGeometry(x_left, 570, 125, 30)
        self.input_pg_occupation.setStyleSheet(self.line_edit_style)

        self.label_pg_contact = QLabel("Contact Number", self)
        self.label_pg_contact.setGeometry(x_right, 550, 125, 20)
        self.label_pg_contact.setStyleSheet(self.field_label_style)

        self.input_pg_contact = QLineEdit(self)
        self.input_pg_contact.setGeometry(x_right, 570, 125, 30)
        self.input_pg_contact.setStyleSheet(self.line_edit_style)

        # Address (long)
        self.label_pg_address = QLabel("Address", self)
        self.label_pg_address.setGeometry(450, 610, 300, 20)
        self.label_pg_address.setStyleSheet(self.field_label_style)

        self.input_pg_address = QLineEdit(self)
        self.input_pg_address.setGeometry(450, 630, 300, 30)
        self.input_pg_address.setStyleSheet(self.line_edit_style)

        # Same as Student checkbox (bottom right of main shape)
        self.checkbox_pg_same = QCheckBox("Same as Student", self)
        self.checkbox_pg_same.setGeometry(635, 670, 150, 20)
        self.checkbox_pg_same.setStyleSheet("""
            QCheckBox {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                                            font-family: Poppins;
                font-size: 10px;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border-radius: 0px;
                border: 1px solid rgb(150, 150, 150);
                background-color: rgb(40, 40, 40);
            }
            QCheckBox::indicator:checked {
                background-color: rgb(234, 234, 234);
                border: 1px solid rgb(234, 234, 234);
            }
        """)
        self.checkbox_pg_same.stateChanged.connect(self._sync_parent_address)

        # Page 2: Cancel at top-left, Back beside Next, Next at bottom-right
        self.button_cancel_2 = QPushButton("CANCEL", self)
        self.button_cancel_2.setGeometry(25, 25, 125, 30)
        self.button_cancel_2.setStyleSheet(self.cancel_button_style)

        self.button_back_2 = QPushButton("BACK", self)
        self.button_back_2.setGeometry(625, 720, 125, 30)
        self.button_back_2.setStyleSheet("""
            QPushButton {
                background-color: rgb(50, 50, 50);
                color: rgb(193, 193, 193);
                border-radius: 0px;
                border: 1px solid rgb(193, 193, 193);
                padding: 2px 6px;
                font-family: Poppins;
                font-size: 12px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: rgb(70, 70, 70);
            }
            QPushButton:pressed {
                background-color: rgb(40, 40, 40);
            }
        """)

        self.button_next_2 = QPushButton("NEXT", self)
        self.button_next_2.setGeometry(775, 720, 125, 30)
        self.button_next_2.setStyleSheet(self.primary_button_style)

        self.button_cancel_2.clicked.connect(self._on_cancel_clicked)
        self.button_back_2.clicked.connect(lambda: self._set_page(1))
        self.button_next_2.clicked.connect(lambda: self._set_page(3))

    def _build_page3_academic_documents(self):
        # Academic Information title
        self.page3_title_academic = QLabel("ACADEMIC INFORMATION", self)
        self.page3_title_academic.setGeometry(450, 150, 300, 25)
        self.page3_title_academic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page3_title_academic.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                                            font-family: Poppins;
                font-size: 16px;
                font-weight: normal;
            }
        """)

        # Long dropdowns: School Year, Grade Level, Track, Strand
        self.label_school_year = QLabel("School Year", self)
        self.label_school_year.setGeometry(450, 200, 300, 20)
        self.label_school_year.setStyleSheet(self.field_label_style)

        self.combo_school_year = QComboBox(self)
        self.combo_school_year.setGeometry(450, 220, 300, 30)
        self.combo_school_year.addItems(["2025-2026", "2026-2027"])
        self.combo_school_year.setStyleSheet(self.combo_style)

        self.label_grade_level = QLabel("Grade Level", self)
        self.label_grade_level.setGeometry(450, 260, 300, 20)
        self.label_grade_level.setStyleSheet(self.field_label_style)

        self.combo_grade_level = QComboBox(self)
        self.combo_grade_level.setGeometry(450, 280, 300, 30)
        self.combo_grade_level.addItems(["Grade 11", "Grade 12"])
        self.combo_grade_level.setStyleSheet(self.combo_style)

        self.label_track = QLabel("Track", self)
        self.label_track.setGeometry(450, 320, 300, 20)
        self.label_track.setStyleSheet(self.field_label_style)

        self.combo_track = QComboBox(self)
        self.combo_track.setGeometry(450, 340, 300, 30)
        self.combo_track.addItems(["Academic", "TVL"])
        self.combo_track.setStyleSheet(self.combo_style)

        self.label_strand = QLabel("Strand", self)
        self.label_strand.setGeometry(450, 380, 300, 20)
        self.label_strand.setStyleSheet(self.field_label_style)

        self.combo_strand = QComboBox(self)
        self.combo_strand.setGeometry(450, 400, 300, 30)
        self.combo_strand.setStyleSheet(self.combo_style)
        self._update_strand_options(self.combo_track.currentText())
        self.combo_track.currentTextChanged.connect(self._update_strand_options)

        # Submit Documents title
        self.page3_title_docs = QLabel("SUBMIT DOCUMENTS", self)
        self.page3_title_docs.setGeometry(450, 455, 300, 25)
        self.page3_title_docs.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page3_title_docs.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                                        font-family: Poppins;
                font-size: 16px;
                font-weight: normal;
            }
        """)

        # File selection structure
        self.selected_files = {
            "Form 137": None,
            "Birth Certificate": None,
            "Report Card": None,
            "Good Moral": None,
        }

        docs = [
            ("Form 137", 505),
            ("Birth Certificate", 530),
            ("Report Card", 555),
            ("Good Moral", 580),
        ]

        self.doc_checkboxes = {}
        self.doc_buttons = {}

        for name, y in docs:
            checkbox = QCheckBox(name, self)
            checkbox.setGeometry(450, y, 125, 15)
            checkbox.setEnabled(False)  # Read-only, only checked when file selected
            checkbox.setStyleSheet("""
                QCheckBox {
                    background-color: rgba(0, 0, 0, 0);
                    border: none;
                    color: rgb(234, 234, 234);
                                        font-family: Poppins;
                    font-size: 10px;
                }
                QCheckBox::indicator {
                    width: 13px;
                    height: 13px;
                    border-radius: 0px;
                    border: 1px solid rgb(150, 150, 150);
                    background-color: rgb(40, 40, 40);
                }
                QCheckBox::indicator:checked {
                    background-color: rgb(234, 234, 234);
                    border: 1px solid rgb(234, 234, 234);
                }
                QCheckBox::indicator:disabled {
                    border: 1px solid rgb(150, 150, 150);
                    background-color: rgb(40, 40, 40);
                }
                QCheckBox::indicator:disabled:checked {
                    background-color: rgb(234, 234, 234);
                    border: 1px solid rgb(234, 234, 234);
                }
            """)

            button = QPushButton("Select File", self)
            button.setGeometry(625, y, 125, 15)
            button.setStyleSheet("""
                                    QPushButton {
                    background-color: rgb(193, 193, 193);
                    color: rgb(50, 50, 50);
                    border-radius: 0px;
                    border: 1px solid rgb(132, 132, 132);
                    padding: 1px 4px;
                                        font-family: Poppins;
                    font-size: 10px;
                    font-weight: normal;
                                        }
                                    QPushButton:hover {
                    background-color: rgb(255, 255, 255);
                                        }
                                    QPushButton:pressed {
                    background-color: rgb(175, 175, 175);
                }
            """)

            button.clicked.connect(lambda _, n=name: self._pick_file(n))

            self.doc_checkboxes[name] = checkbox
            self.doc_buttons[name] = button

        # Page 3: Cancel at top-left, Back beside Next, Next at bottom-right
        self.button_cancel_3 = QPushButton("CANCEL", self)
        self.button_cancel_3.setGeometry(25, 25, 125, 30)
        self.button_cancel_3.setStyleSheet(self.cancel_button_style)

        self.button_back_3 = QPushButton("BACK", self)
        self.button_back_3.setGeometry(625, 720, 125, 30)
        self.button_back_3.setStyleSheet("""
            QPushButton {
                background-color: rgb(50, 50, 50);
                color: rgb(193, 193, 193);
                border-radius: 0px;
                border: 1px solid rgb(193, 193, 193);
                padding: 2px 6px;
                font-family: Poppins;
                font-size: 12px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: rgb(70, 70, 70);
            }
            QPushButton:pressed {
                background-color: rgb(40, 40, 40);
            }
        """)

        self.button_next_3 = QPushButton("NEXT", self)
        self.button_next_3.setGeometry(775, 720, 125, 30)
        self.button_next_3.setStyleSheet(self.primary_button_style)

        self.button_cancel_3.clicked.connect(self._on_cancel_clicked)
        self.button_back_3.clicked.connect(lambda: self._set_page(2))
        self.button_next_3.clicked.connect(lambda: self._set_page(4))

    def _build_page4_account_credentials(self):
        # Title
        self.page4_title = QLabel("ACCOUNT CREDENTIALS", self)
        self.page4_title.setGeometry(450, 150, 300, 25)
        self.page4_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page4_title.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                                    font-family: Poppins;
                font-size: 16px;
                font-weight: normal;
            }
        """)

        # Username
        self.label_username = QLabel("Username", self)
        self.label_username.setGeometry(450, 200, 300, 20)
        self.label_username.setStyleSheet(self.field_label_style)

        self.input_username = QLineEdit(self)
        self.input_username.setGeometry(450, 220, 300, 30)
        self.input_username.setStyleSheet(self.line_edit_style)

        # Password
        self.label_password = QLabel("Password", self)
        self.label_password.setGeometry(450, 260, 300, 20)
        self.label_password.setStyleSheet(self.field_label_style)

        self.input_password = QLineEdit(self)
        self.input_password.setGeometry(450, 280, 300, 30)
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setStyleSheet(self.line_edit_style)

        # Confirm Password
        self.label_confirm_password = QLabel("Confirm Password", self)
        self.label_confirm_password.setGeometry(450, 320, 300, 20)
        self.label_confirm_password.setStyleSheet(self.field_label_style)

        self.input_confirm_password = QLineEdit(self)
        self.input_confirm_password.setGeometry(450, 340, 300, 30)
        self.input_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_confirm_password.setStyleSheet(self.line_edit_style)

        # Security Question
        self.label_security_question = QLabel("Security Question", self)
        self.label_security_question.setGeometry(450, 380, 300, 20)
        self.label_security_question.setStyleSheet(self.field_label_style)

        self.combo_security_question = QComboBox(self)
        self.combo_security_question.setGeometry(450, 400, 300, 30)
        self.combo_security_question.addItems([
            "What is your favorite color?",
            "What is your favorite food?",
            "What is your favorite animal",
        ])
        self.combo_security_question.setStyleSheet(self.combo_style)

        # Security Answer
        self.label_security_answer = QLabel("Security Answer", self)
        self.label_security_answer.setGeometry(450, 440, 300, 20)
        self.label_security_answer.setStyleSheet(self.field_label_style)

        self.input_security_answer = QLineEdit(self)
        self.input_security_answer.setGeometry(450, 460, 300, 30)
        self.input_security_answer.setStyleSheet(self.line_edit_style)

        # Consent checkbox + text
        self.checkbox_consent = QCheckBox("", self)
        self.checkbox_consent.setGeometry(450, 515, 15, 15)
        self.checkbox_consent.setStyleSheet("""
            QCheckBox {
                background-color: rgba(0, 0, 0, 0);
                border: none;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border-radius: 0px;
                border: 1px solid rgb(150, 150, 150);
                background-color: rgb(40, 40, 40);
            }
            QCheckBox::indicator:checked {
                background-color: rgb(234, 234, 234);
                border: 1px solid rgb(234, 234, 234);
            }
        """)

        self.label_consent_text = QLabel(self)
        self.label_consent_text.setGeometry(465, 500, 285, 50)
        self.label_consent_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_consent_text.setWordWrap(True)
        self.label_consent_text.setText(
            "I agree to the Terms and Conditions and consent to the processing of my personal data as described in the Privacy Policy."
        )
        self.label_consent_text.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                                        font-family: Poppins;
                font-size: 10px;
                font-weight: normal;
            }
        """)

        # Page 4: Cancel at top-left, Back beside Submit, Submit at bottom-right
        self.button_cancel_4 = QPushButton("CANCEL", self)
        self.button_cancel_4.setGeometry(25, 25, 125, 30)
        self.button_cancel_4.setStyleSheet(self.cancel_button_style)

        self.button_back_4 = QPushButton("BACK", self)
        self.button_back_4.setGeometry(625, 720, 125, 30)
        self.button_back_4.setStyleSheet("""
            QPushButton {
                background-color: rgb(50, 50, 50);
                color: rgb(193, 193, 193);
                border-radius: 0px;
                border: 1px solid rgb(193, 193, 193);
                padding: 2px 6px;
                font-family: Poppins;
                font-size: 12px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: rgb(70, 70, 70);
            }
            QPushButton:pressed {
                background-color: rgb(40, 40, 40);
            }
        """)

        self.button_submit = QPushButton("SUBMIT", self)
        self.button_submit.setGeometry(775, 720, 125, 30)
        self.button_submit.setStyleSheet("""
            QPushButton {
                background-color: rgb(0, 132, 0);
                color: rgb(234, 234, 234);
                border-radius: 0px;
                border: 1px solid rgb(0, 100, 0);
                padding: 6px 10px;
                font-family: Poppins;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(0, 180, 0);
            }
            QPushButton:pressed {
                background-color: rgb(0, 100, 0);
            }
            QPushButton:disabled {
                background-color: rgb(90, 90, 90);
                color: rgb(160, 160, 160);
            }
        """)

        self.button_cancel_4.clicked.connect(self._on_cancel_clicked)
        self.button_back_4.clicked.connect(lambda: self._set_page(3))
        self.button_submit.clicked.connect(self._on_submit_clicked)

    def _set_page(self, page: int):
        self.current_page = page
        # Helper to show/hide widgets for each page
        page1_widgets = [
            self.page1_title,
            self.label_lrn, self.input_lrn,
            self.label_first_name, self.input_first_name,
            self.label_email, self.input_email,
            self.label_middle_name, self.input_middle_name,
            self.label_last_name, self.input_last_name,
            self.label_suffix, self.input_suffix,
            self.label_age, self.input_age,
            self.label_gender, self.input_gender,
            self.label_birthdate, self.input_birthdate,
            self.label_nationality, self.input_nationality,
            self.label_religion, self.input_religion,
            self.label_civil_status, self.input_civil_status,
            self.label_contact_number, self.input_contact_number,
            self.button_cancel_1, self.button_next_1,
        ]

        page2_widgets = [
            self.page2_title_address,
            self.label_house, self.input_house,
            self.label_barangay, self.input_barangay,
            self.label_city, self.input_city,
            self.label_province, self.input_province,
            self.label_zip, self.input_zip,
            self.page2_title_parent,
            self.label_pg_fullname, self.input_pg_fullname,
            self.label_pg_relationship, self.input_pg_relationship,
            self.label_pg_occupation, self.input_pg_occupation,
            self.label_pg_contact, self.input_pg_contact,
            self.label_pg_address, self.input_pg_address,
            self.checkbox_pg_same,
            self.button_cancel_2, self.button_back_2, self.button_next_2,
        ]

        page3_widgets = [
            self.page3_title_academic,
            self.label_school_year, self.combo_school_year,
            self.label_grade_level, self.combo_grade_level,
            self.label_track, self.combo_track,
            self.label_strand, self.combo_strand,
            self.page3_title_docs,
            *self.doc_checkboxes.values(),
            *self.doc_buttons.values(),
            self.button_cancel_3, self.button_back_3, self.button_next_3,
        ]

        page4_widgets = [
            self.page4_title,
            self.label_username, self.input_username,
            self.label_password, self.input_password,
            self.label_confirm_password, self.input_confirm_password,
            self.label_security_question, self.combo_security_question,
            self.label_security_answer, self.input_security_answer,
            self.checkbox_consent, self.label_consent_text,
            self.button_cancel_4, self.button_back_4, self.button_submit,
        ]

        all_pages = [page1_widgets, page2_widgets, page3_widgets, page4_widgets]

        for idx, widgets in enumerate(all_pages, start=1):
            visible = (idx == page)
            for w in widgets:
                w.setVisible(visible)

    def _on_back_top_clicked(self):
        # Back through pages; from first page, ask if user wants to cancel to login
        if self.current_page > 1:
            self._set_page(self.current_page - 1)
        else:
            self._on_cancel_clicked()

    def _on_cancel_clicked(self):
        confirm = QMessageBox.question(
            self,
            "Cancel Registration",
            "Are you sure you want to cancel? All data will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self._set_page(1)
            self.main_window.switch_view("login")

    def _on_next_clicked_page1(self):
        self._set_page(2)

    def _sync_parent_address(self):
        if self.checkbox_pg_same.isChecked():
            parts = [
                self.input_house.text().strip(),
                self.input_barangay.text().strip(),
                self.input_city.text().strip(),
                self.input_province.text().strip(),
                self.input_zip.text().strip(),
            ]
            addr = ", ".join(p for p in parts if p)
            self.input_pg_address.setText(addr)
            self.input_pg_address.setEnabled(False)
        else:
            self.input_pg_address.clear()
            self.input_pg_address.setEnabled(True)

    def _update_strand_options(self, track: str):
        self.combo_strand.clear()
        if track == "Academic":
            self.combo_strand.addItems(["STEM", "HUMSS", "ABM", "GAS"])
        elif track == "TVL":
            self.combo_strand.addItems(["ICT", "HE", "IA"])

    def _pick_file(self, doc_name: str):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Select {doc_name}",
            "",
            "PDF Files (*.pdf *.txt);;Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.selected_files[doc_name] = file_path
            self.doc_checkboxes[doc_name].setChecked(True)
        else:
            self.selected_files[doc_name] = None
            self.doc_checkboxes[doc_name].setChecked(False)
    
    def _setup_validation(self):
        """Setup input validation for data types"""
        # LRN: max 12 characters, alphanumeric
        self.input_lrn.textChanged.connect(lambda: self._validate_lrn())
        
        # Age: must be integer, 1-150
        self.input_age.textChanged.connect(lambda: self._validate_age())
        
        # Contact Number: max 20 characters, numeric
        self.input_contact_number.textChanged.connect(lambda: self._validate_contact())
        self.input_pg_contact.textChanged.connect(lambda: self._validate_contact_pg())
        
        # Email: valid email format
        self.input_email.textChanged.connect(lambda: self._validate_email())
        
        # ZIP: max 10 characters
        self.input_zip.textChanged.connect(lambda: self._validate_zip())
        
        # Name fields: max 50 characters
        self.input_first_name.textChanged.connect(lambda: self._validate_name(self.input_first_name, 50))
        self.input_middle_name.textChanged.connect(lambda: self._validate_name(self.input_middle_name, 50))
        self.input_last_name.textChanged.connect(lambda: self._validate_name(self.input_last_name, 50))
        self.input_pg_fullname.textChanged.connect(lambda: self._validate_name(self.input_pg_fullname, 100))
        
        # Nationality, Religion: max 50 characters
        self.input_nationality.textChanged.connect(lambda: self._validate_name(self.input_nationality, 50))
        self.input_religion.textChanged.connect(lambda: self._validate_name(self.input_religion, 50))
        
        # Civil Status: max 20 characters
        self.input_civil_status.textChanged.connect(lambda: self._validate_name(self.input_civil_status, 20))
    
    def _validate_lrn(self):
        text = self.input_lrn.text()
        if len(text) > 12:
            self.input_lrn.setText(text[:12])
        # Only allow alphanumeric
        if text and not re.match(r'^[A-Za-z0-9]*$', text):
            cursor = self.input_lrn.cursorPosition()
            self.input_lrn.setText(re.sub(r'[^A-Za-z0-9]', '', text))
            self.input_lrn.setCursorPosition(min(cursor - 1, len(self.input_lrn.text())))
    
    def _validate_age(self):
        """Only allow numeric input, but don't clamp values - validation happens on submit"""
        text = self.input_age.text()
        if text and not text.isdigit():
            cursor = self.input_age.cursorPosition()
            self.input_age.setText(re.sub(r'[^0-9]', '', text))
            self.input_age.setCursorPosition(min(cursor - 1, len(self.input_age.text())))
    
    def _validate_contact(self):
        text = self.input_contact_number.text()
        if len(text) > 20:
            self.input_contact_number.setText(text[:20])
        # Allow digits, spaces, dashes, parentheses for phone numbers
        if text and not re.match(r'^[0-9\s\-\(\)]*$', text):
            cursor = self.input_contact_number.cursorPosition()
            self.input_contact_number.setText(re.sub(r'[^0-9\s\-\(\)]', '', text))
            self.input_contact_number.setCursorPosition(min(cursor - 1, len(self.input_contact_number.text())))
    
    def _validate_contact_pg(self):
        text = self.input_pg_contact.text()
        if len(text) > 20:
            self.input_pg_contact.setText(text[:20])
        if text and not re.match(r'^[0-9\s\-\(\)]*$', text):
            cursor = self.input_pg_contact.cursorPosition()
            self.input_pg_contact.setText(re.sub(r'[^0-9\s\-\(\)]', '', text))
            self.input_pg_contact.setCursorPosition(min(cursor - 1, len(self.input_pg_contact.text())))
    
    def _validate_email(self):
        text = self.input_email.text()
        if len(text) > 100:
            self.input_email.setText(text[:100])
    
    def _validate_zip(self):
        text = self.input_zip.text()
        if len(text) > 10:
            self.input_zip.setText(text[:10])
    
    def _validate_name(self, widget, max_len):
        text = widget.text()
        if len(text) > max_len:
            widget.setText(text[:max_len])

    def _on_submit_clicked(self):
        if not self.checkbox_consent.isChecked():
            QMessageBox.warning(self, "Consent Required", "You must agree to the terms and conditions to continue.")
            return

        valid, message = self._validate_fields()
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Submission",
            "Submit registration and create account?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            data = self._collect_form_data()

            account_id = self.auth_controller.register_account(
                username=data["account"]["username"],
                password=data["account"]["password"],
                role="student",
                security_question=data["account"]["security_question"],
                security_answer=data["account"]["security_answer"]
            )

            if not account_id:
                QMessageBox.critical(
                    self,
                    "Registration Failed",
                    "Failed to create account. Username may already exist."
                )
                return

            data["student"]["account_id"] = account_id

            student_id = self.controller.create_student_record(
                student_data=data["student"],
                address_data=data["address"],
                academic_data=data["academic"],
                parent_data=data["parent_guardian"]
            )

            if not student_id:
                QMessageBox.critical(
                    self,
                    "Registration Failed",
                    "Failed to create student record."
                )
                return

            documents = []
            for doc_type, file_path in self.selected_files.items():
                if file_path:
                    documents.append({
                        "DocumentType": doc_type,
                        "FilePath": file_path
                    })

            registration_id = self.main_window.registration_model.create_registration(
                student_id=student_id,
                grade_level=data["academic"]["GradeLevel"],
                track=data["academic"]["Track"],
                strand=data["academic"]["Strand"],
                school_year=data["school_year"],
                documents=documents if documents else None
            )

            if not registration_id:
                QMessageBox.warning(
                    self,
                    "Registration Warning",
                    "Student created but registration record failed. Please contact administrator."
                )
            else:
                QMessageBox.information(
                    self,
                    "Success",
                    "Registration completed successfully."
                )
                self.main_window.current_user = {
                    "role": "student",
                    "account_id": account_id
                }
                if hasattr(self.main_window.views["student_dashboard"], "load_student_data"):
                    self.main_window.views["student_dashboard"].load_student_data(account_id)

            self.main_window.switch_view("student_dashboard")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Registration Failed",
                f"{str(e)}"
            )

    def _validate_fields(self):
        required_edits = [
            self.input_lrn,
            self.input_first_name,
            self.input_last_name,
            self.input_age,
            self.input_nationality,
            self.input_contact_number,
            self.input_email,
            self.input_username,
            self.input_password,
            self.input_confirm_password,
            self.input_security_answer,
        ]

        for e in required_edits:
            if not e.text().strip():
                return False, "Please fill in all required fields."

        if self.input_password.text() != self.input_confirm_password.text():
            return False, "Passwords do not match."

        # Validate data types
        # Age: must be integer between 1-150
        try:
            age = int(self.input_age.text().strip())
            if age < 1 or age > 150:
                return False, "Age must be between 1 and 150."
        except ValueError:
            return False, "Age must be a valid integer."

        # LRN: max 12 characters, alphanumeric
        lrn = self.input_lrn.text().strip()
        if len(lrn) > 12:
            return False, "LRN must be 12 characters or less."
        if not re.match(r'^[A-Za-z0-9]+$', lrn):
            return False, "LRN must contain only letters and numbers."

        # Contact Number: max 20 characters
        if len(self.input_contact_number.text().strip()) > 20:
            return False, "Contact number must be 20 characters or less."
        
        # Parent/Guardian Contact: max 20 characters
        if len(self.input_pg_contact.text().strip()) > 20:
            return False, "Parent/Guardian contact number must be 20 characters or less."

        # Email: max 100 characters
        email = self.input_email.text().strip()
        if len(email) > 100:
            return False, "Email must be 100 characters or less."
        # Basic email format validation
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return False, "Please enter a valid email address."

        # ZIP: max 10 characters
        if len(self.input_zip.text().strip()) > 10:
            return False, "ZIP/Postal code must be 10 characters or less."

        # Name fields: max lengths
        if len(self.input_first_name.text().strip()) > 50:
            return False, "First name must be 50 characters or less."
        if len(self.input_middle_name.text().strip()) > 50:
            return False, "Middle name must be 50 characters or less."
        if len(self.input_last_name.text().strip()) > 50:
            return False, "Last name must be 50 characters or less."
        if len(self.input_pg_fullname.text().strip()) > 100:
            return False, "Parent/Guardian name must be 100 characters or less."
        if len(self.input_nationality.text().strip()) > 50:
            return False, "Nationality must be 50 characters or less."
        if len(self.input_religion.text().strip()) > 50:
            return False, "Religion must be 50 characters or less."
        if len(self.input_civil_status.text().strip()) > 20:
            return False, "Civil status must be 20 characters or less."

        for doc_name, path in self.selected_files.items():
            if not path:
                return False, f"Missing required document: {doc_name}"

        return True, ""

    def _collect_form_data(self):
        return {
            "account": {
                "username": self.input_username.text().strip(),
                "password": self.input_password.text(),
                "security_question": self.combo_security_question.currentText(),
                "security_answer": self.input_security_answer.text().strip(),
            },
            "student": {
                "lrn": self.input_lrn.text().strip(),
                "first_name": self.input_first_name.text().strip(),
                "middle_name": self.input_middle_name.text().strip() if self.input_middle_name.text() else None,
                "last_name": self.input_last_name.text().strip(),
                "suffix": self.input_suffix.text().strip() if self.input_suffix.text() else None,
                "gender": self.input_gender.currentText(),
                "birthdate": self.input_birthdate.date().toPyDate(),
                "age": int(self.input_age.text()),
                "nationality": self.input_nationality.text().strip(),
                "religion": self.input_religion.text().strip(),
                "civil_status": self.input_civil_status.text().strip(),
                "contact_num": self.input_contact_number.text().strip(),
                "email": self.input_email.text().strip(),
            },
            "address": {
                "HouseNum": self.input_house.text().strip(),
                "Barangay": self.input_barangay.text().strip(),
                "City": self.input_city.text().strip(),
                "Province": self.input_province.text().strip(),
                "ZIP": self.input_zip.text().strip(),
            },
            "parent_guardian": {
                "Name": self.input_pg_fullname.text().strip(),
                "Relationship": self.input_pg_relationship.text().strip(),
                "Occupation": self.input_pg_occupation.text().strip(),
                "ContactNum": self.input_pg_contact.text().strip(),
                "Address": self.input_pg_address.text().strip(),
            },
            "academic": {
                "GradeLevel": self.combo_grade_level.currentText(),
                "Track": self.combo_track.currentText(),
                "Strand": self.combo_strand.currentText(),
            },
            "school_year": self.combo_school_year.currentText(),
        }

