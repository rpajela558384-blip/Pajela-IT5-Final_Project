from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, \
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QScrollArea, QComboBox, QDateEdit, QFileDialog
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QRect, QDate
import os
import subprocess
import platform

class StudentSummary(QWidget):
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
        pixmap = pixmap.scaled(120, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setGeometry(25, 20, 120, 40)

        # Drop Shadow Effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(10)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 160))

        self.shape1 = QWidget(self)
        self.shape1.setGeometry(200, 100, 800, 600)
        self.shape1.setStyleSheet(
            "background-color:rgb(60, 60, 60); border-radius:0px; border: 1px solid rgba(200, 0, 0, 50);")
        self.shape1.show()
        self.shape1.setGraphicsEffect(shadow)

        self.shape2 = QWidget(self)
        self.shape2.setGeometry(425, 75, 350, 50)
        self.shape2.setStyleSheet(
            "background-color:rgb(120, 0, 0); border-radius:0px; border: 1px solid rgb(50,50,50);")
        self.shape2.show()

        self.header = QLabel("Registration Summary", self.shape2)
        self.header.setGeometry(55, 10, 250, 30)
        self.header.setStyleSheet("""
                                                    QLabel {
                                                        background-color: rgba(200, 200, 0, 0);
                                                        border: 1px solid rgba(0,0,0,0);
                                                        color: rgb(200, 200, 200);
                                                        font-family: Poppins;
                                                        font-size: 20px;
                                                        font-weight: bold;
                                                        }""")

        self.back = QPushButton(self)
        self.back.setText("BACK")
        self.back.setGeometry(25, 25, 125, 30)
        self.back.setStyleSheet("""
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
                                        background-color: rgb(60, 60, 60);
                                        border: 1px solid rgba(255, 255, 255, 0);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(40, 40, 40);
                                        border: 2px solid rgba(255, 255, 255, 0);
                                        }""")

        # Scroll area
        self.scroll = QScrollArea(self)
        self.scroll.setGeometry(230, 125, 750, 550)
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(
            "background-color:rgb(60, 60, 60); border-radius:0px; border: 1px solid rgba(200, 0, 0, 0);")
        self.scroll.show()

        self.shape_content = QWidget()
        self.shape_content.setFixedSize(735, 1000)  # Reduced height
        self.scroll.setWidget(self.shape_content)

        # Common style for read-only fields - disabled, no focus, proper padding
        self.readonly_style = """
            QLineEdit {
                background-color: rgb(50, 50, 50);
                border: 1px solid rgba(150, 150, 150, 0);
                border-radius: 0px;
                padding: 5px 12px;
                color: rgb(225, 225, 225);
                font-family: Poppins;
                font-size: 12px;
                }
            QLineEdit:disabled {
                background-color: rgb(50, 50, 50);
                color: rgb(225, 225, 225);
                border: 1px solid rgba(150, 150, 150, 0);
                }"""

        # Label style without underline
        label_style = """
                    QLabel {
                        background-color: rgba(152, 152, 152, 0);
                        border: 1px solid rgba(0,0,0,0);
                        color: rgb(200, 200, 200);
                        font-family: Poppins;
                        font-size: 18px;
                        font-weight: regular;
                        }"""

        # Section labels
        self.label1 = QLabel("Personal Information", self.shape_content)
        self.label1.setGeometry(50, 10, 300, 30)
        self.label1.setStyleSheet(label_style)

        # Personal Information Fields with labels
        self.lrn_label = QLabel("LRN", self.shape_content)
        self.lrn_label.setGeometry(50, 50, 300, 20)
        self.lrn_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.lrn = QLineEdit(self.shape_content)
        self.lrn.setReadOnly(True)
        self.lrn.setEnabled(False)
        self.lrn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lrn.setStyleSheet(self.readonly_style)
        self.lrn.setGeometry(50, 70, 300, 35)

        self.full_name_label = QLabel("Full Name", self.shape_content)
        self.full_name_label.setGeometry(375, 50, 300, 20)
        self.full_name_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.full_name = QLineEdit(self.shape_content)
        self.full_name.setReadOnly(True)
        self.full_name.setEnabled(False)
        self.full_name.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.full_name.setStyleSheet(self.readonly_style)
        self.full_name.setGeometry(375, 70, 300, 35)

        self.gender_label = QLabel("Gender", self.shape_content)
        self.gender_label.setGeometry(50, 110, 175, 20)
        self.gender_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.gender = QLineEdit(self.shape_content)
        self.gender.setReadOnly(True)
        self.gender.setEnabled(False)
        self.gender.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gender.setStyleSheet(self.readonly_style)
        self.gender.setGeometry(50, 130, 175, 35)

        self.age_label = QLabel("Age", self.shape_content)
        self.age_label.setGeometry(250, 110, 100, 20)
        self.age_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.age = QLineEdit(self.shape_content)
        self.age.setReadOnly(True)
        self.age.setEnabled(False)
        self.age.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.age.setStyleSheet(self.readonly_style)
        self.age.setGeometry(250, 130, 100, 35)

        self.birthdate_label = QLabel("Birthdate", self.shape_content)
        self.birthdate_label.setGeometry(375, 110, 175, 20)
        self.birthdate_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.birthdate = QLineEdit(self.shape_content)
        self.birthdate.setReadOnly(True)
        self.birthdate.setEnabled(False)
        self.birthdate.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.birthdate.setStyleSheet(self.readonly_style)
        self.birthdate.setGeometry(375, 130, 175, 35)

        self.nationality_label = QLabel("Nationality", self.shape_content)
        self.nationality_label.setGeometry(575, 110, 100, 20)
        self.nationality_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.nationality = QLineEdit(self.shape_content)
        self.nationality.setReadOnly(True)
        self.nationality.setEnabled(False)
        self.nationality.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.nationality.setStyleSheet(self.readonly_style)
        self.nationality.setGeometry(575, 130, 100, 30)

        self.religion_label = QLabel("Religion", self.shape_content)
        self.religion_label.setGeometry(50, 170, 300, 20)
        self.religion_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.religion = QLineEdit(self.shape_content)
        self.religion.setReadOnly(True)
        self.religion.setEnabled(False)
        self.religion.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.religion.setStyleSheet(self.readonly_style)
        self.religion.setGeometry(50, 190, 300, 35)

        self.civil_status_label = QLabel("Civil Status", self.shape_content)
        self.civil_status_label.setGeometry(375, 170, 300, 20)
        self.civil_status_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.civil_status = QLineEdit(self.shape_content)
        self.civil_status.setReadOnly(True)
        self.civil_status.setEnabled(False)
        self.civil_status.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.civil_status.setStyleSheet(self.readonly_style)
        self.civil_status.setGeometry(375, 190, 300, 35)

        self.contact_number_label = QLabel("Contact Number", self.shape_content)
        self.contact_number_label.setGeometry(50, 230, 300, 20)
        self.contact_number_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.contact_number = QLineEdit(self.shape_content)
        self.contact_number.setReadOnly(True)
        self.contact_number.setEnabled(False)
        self.contact_number.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.contact_number.setStyleSheet(self.readonly_style)
        self.contact_number.setGeometry(50, 250, 300, 35)

        self.email_label = QLabel("Email", self.shape_content)
        self.email_label.setGeometry(375, 230, 300, 20)
        self.email_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.email = QLineEdit(self.shape_content)
        self.email.setReadOnly(True)
        self.email.setEnabled(False)
        self.email.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.email.setStyleSheet(self.readonly_style)
        self.email.setGeometry(375, 250, 300, 35)

        # Address Information - 25px from last field (250+30+25=305)
        self.label2 = QLabel("Address Information", self.shape_content)
        self.label2.setGeometry(50, 305, 300, 30)
        self.label2.setStyleSheet(label_style)
        
        self.full_address_label = QLabel("Full Address", self.shape_content)
        self.full_address_label.setGeometry(50, 345, 625, 20)
        self.full_address_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.full_address = QLineEdit(self.shape_content)
        self.full_address.setReadOnly(True)
        self.full_address.setEnabled(False)
        self.full_address.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.full_address.setStyleSheet(self.readonly_style)
        self.full_address.setGeometry(50, 365, 625, 35)

        # Parent/Guardian Information - 25px from last field (365+30+25=420)
        self.label3 = QLabel("Parent / Guardian Information", self.shape_content)
        self.label3.setGeometry(50, 420, 300, 30)
        self.label3.setStyleSheet(label_style)
        
        self.pg_name_label = QLabel("Parent / Guardian Name", self.shape_content)
        self.pg_name_label.setGeometry(50, 460, 300, 20)
        self.pg_name_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.pg_name = QLineEdit(self.shape_content)
        self.pg_name.setReadOnly(True)
        self.pg_name.setEnabled(False)
        self.pg_name.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pg_name.setStyleSheet(self.readonly_style)
        self.pg_name.setGeometry(50, 480, 300, 35)

        self.relationship_label = QLabel("Relationship", self.shape_content)
        self.relationship_label.setGeometry(375, 460, 300, 20)
        self.relationship_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.relationship = QLineEdit(self.shape_content)
        self.relationship.setReadOnly(True)
        self.relationship.setEnabled(False)
        self.relationship.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.relationship.setStyleSheet(self.readonly_style)
        self.relationship.setGeometry(375, 480, 300, 35)

        self.occupation_label = QLabel("Occupation", self.shape_content)
        self.occupation_label.setGeometry(50, 520, 300, 20)
        self.occupation_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.occupation = QLineEdit(self.shape_content)
        self.occupation.setReadOnly(True)
        self.occupation.setEnabled(False)
        self.occupation.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.occupation.setStyleSheet(self.readonly_style)
        self.occupation.setGeometry(50, 540, 300, 35)

        self.pg_contact_label = QLabel("Contact Number", self.shape_content)
        self.pg_contact_label.setGeometry(375, 520, 300, 20)
        self.pg_contact_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.pg_contact = QLineEdit(self.shape_content)
        self.pg_contact.setReadOnly(True)
        self.pg_contact.setEnabled(False)
        self.pg_contact.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pg_contact.setStyleSheet(self.readonly_style)
        self.pg_contact.setGeometry(375, 540, 300, 35)

        self.pg_address_label = QLabel("Address", self.shape_content)
        self.pg_address_label.setGeometry(50, 580, 625, 20)
        self.pg_address_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.pg_address = QLineEdit(self.shape_content)
        self.pg_address.setReadOnly(True)
        self.pg_address.setEnabled(False)
        self.pg_address.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pg_address.setStyleSheet(self.readonly_style)
        self.pg_address.setGeometry(50, 600, 625, 35)

        # Academic Information - 25px from last field (600+30+25=655)
        self.label4 = QLabel("Academic Information", self.shape_content)
        self.label4.setGeometry(50, 655, 300, 30)
        self.label4.setStyleSheet(label_style)
        
        self.grade_level_label = QLabel("Grade Level", self.shape_content)
        self.grade_level_label.setGeometry(50, 695, 300, 20)
        self.grade_level_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.grade_level = QLineEdit(self.shape_content)
        self.grade_level.setReadOnly(True)
        self.grade_level.setEnabled(False)
        self.grade_level.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.grade_level.setStyleSheet(self.readonly_style)
        self.grade_level.setGeometry(50, 715, 300, 35)

        self.school_year_label = QLabel("School Year", self.shape_content)
        self.school_year_label.setGeometry(375, 695, 300, 20)
        self.school_year_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.school_year = QLineEdit(self.shape_content)
        self.school_year.setReadOnly(True)
        self.school_year.setEnabled(False)
        self.school_year.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.school_year.setStyleSheet(self.readonly_style)
        self.school_year.setGeometry(375, 715, 300, 35)

        self.track_label = QLabel("Track", self.shape_content)
        self.track_label.setGeometry(50, 755, 300, 20)
        self.track_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.track = QLineEdit(self.shape_content)
        self.track.setReadOnly(True)
        self.track.setEnabled(False)
        self.track.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.track.setStyleSheet(self.readonly_style)
        self.track.setGeometry(50, 775, 300, 35)

        self.strand_label = QLabel("Strand", self.shape_content)
        self.strand_label.setGeometry(375, 755, 300, 20)
        self.strand_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 12px; }")
        self.strand = QLineEdit(self.shape_content)
        self.strand.setReadOnly(True)
        self.strand.setEnabled(False)
        self.strand.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.strand.setStyleSheet(self.readonly_style)
        self.strand.setGeometry(375, 775, 300, 35)

        # Document buttons - 25px from last field (775+30+25=830), then 10px to first button (840)
        self.form137 = QPushButton(self.shape_content)
        self.form137.setText("Form 137")
        self.form137.setGeometry(50, 870, 300, 30)
        self.form137.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgba(150, 150, 150, 0);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 255);
                                        padding: 2px 2px;
                                        font-family: Poppins;
                                        font-size: 14px;
                                        font-weight: medium;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(70, 70, 70);
                                        border: 1px solid rgb(255, 255, 255);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(50, 50, 50);
                                        border: 2px solid rgb(255, 255, 255);
                                        }""")

        self.birth_certificate = QPushButton(self.shape_content)
        self.birth_certificate.setText("Birth Certificate")
        self.birth_certificate.setGeometry(375, 870, 300, 30)
        self.birth_certificate.setStyleSheet(self.form137.styleSheet())

        self.report_card = QPushButton(self.shape_content)
        self.report_card.setText("Report Card")
        self.report_card.setGeometry(50, 910, 300, 30)
        self.report_card.setStyleSheet(self.form137.styleSheet())

        self.good_moral = QPushButton(self.shape_content)
        self.good_moral.setText("Good Moral")
        self.good_moral.setGeometry(375, 910, 300, 30)
        self.good_moral.setStyleSheet(self.form137.styleSheet())
        
        # Update content height
        self.shape_content.setFixedSize(735, 1000)

        # Store document paths
        self.document_paths = {}

        # Connect document buttons
        self.form137.clicked.connect(lambda: self.open_document("Form 137"))
        self.birth_certificate.clicked.connect(lambda: self.open_document("Birth Certificate"))
        self.report_card.clicked.connect(lambda: self.open_document("Report Card"))
        self.good_moral.clicked.connect(lambda: self.open_document("Good Moral"))

        # Connect back button
        self.back.clicked.connect(self.handle_back)

        self.setLayout(layout)

    def open_document(self, doc_type):
        """Open document file from saved path"""
        file_path = self.document_paths.get(doc_type)
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "File Not Found", f"{doc_type} file not found or path is invalid.")
            return

        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', file_path])
            else:  # Linux
                subprocess.call(['xdg-open', file_path])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

    def load_summary_data(self, student_id):
        """Load registration summary data for the student"""
        # Get complete student data
        student_data = self.controller.get_complete_student_data(student_id)
        if not student_data:
            return

        # Get registration data with documents
        registrations = self.controller.get_registration_summary(student_id)
        latest_reg = registrations[0] if registrations else None

        # Personal Information
        self.lrn.setText(student_data.get("LRN") or "N/A")
        
        # Full Name
        first_name = student_data.get("FirstName") or ""
        middle_name = student_data.get("MiddleName") or ""
        last_name = student_data.get("LastName") or ""
        suffix = ""
        full_name_parts = [part for part in [first_name, middle_name, last_name, suffix] if part]
        self.full_name.setText(" ".join(full_name_parts) or "N/A")

        self.gender.setText(student_data.get("Gender") or "N/A")
        self.age.setText(str(student_data.get("Age")) if student_data.get("Age") else "N/A")
        
        birthdate = student_data.get("Birthdate")
        if birthdate:
            if isinstance(birthdate, str):
                self.birthdate.setText(birthdate)
            else:
                self.birthdate.setText(birthdate.strftime("%Y-%m-%d"))
        else:
            self.birthdate.setText("N/A")

        self.nationality.setText(student_data.get("Nationality") or "N/A")
        self.religion.setText(student_data.get("Religion") or "N/A")
        self.civil_status.setText(student_data.get("CivilStatus") or "N/A")
        self.contact_number.setText(student_data.get("ContactNum") or "N/A")
        self.email.setText(student_data.get("Email") or "N/A")

        # Full Address
        house = student_data.get("HouseNum") or ""
        barangay = student_data.get("Barangay") or ""
        city = student_data.get("City") or ""
        province = student_data.get("Province") or ""
        zip_code = student_data.get("ZIP") or ""
        address_parts = [part for part in [house, barangay, city, province, zip_code] if part]
        self.full_address.setText(", ".join(address_parts) or "N/A")

        # Parent/Guardian
        self.pg_name.setText(student_data.get("PGName") or "N/A")
        self.relationship.setText(student_data.get("Relationship") or "N/A")
        self.occupation.setText(student_data.get("Occupation") or "N/A")
        self.pg_contact.setText(student_data.get("PGContact") or "N/A")
        self.pg_address.setText(student_data.get("PGAddress") or "N/A")

        # Academic
        self.grade_level.setText(student_data.get("GradeLevel") or "N/A")
        if latest_reg:
            self.school_year.setText(latest_reg.get("SchoolYear") or "N/A")
        else:
            self.school_year.setText("N/A")
        self.track.setText(student_data.get("Track") or "N/A")
        self.strand.setText(student_data.get("Strand") or "N/A")

        # Documents - get from all registrations
        if registrations:
            # Get all documents from all registrations
            for reg in registrations:
                if reg.get("DocumentType") and reg.get("FilePath"):
                    doc_type = reg.get("DocumentType")
                    file_path = reg.get("FilePath")
                    self.document_paths[doc_type] = file_path

    def handle_back(self):
        """Handle back button click - return to student dashboard"""
        self.main_window.switch_view("student_dashboard")
