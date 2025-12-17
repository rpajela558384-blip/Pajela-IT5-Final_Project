from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, \
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QScrollArea, QComboBox, QDateEdit, QFileDialog
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QRect, QDate
import os
import subprocess
import platform

class RegistrarValidation(QWidget):
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
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files", "Final Logo - White.png")
        pixmap = QPixmap(logo_path)
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
        self.shape1.setGeometry(100, 65, 1000, 650)
        self.shape1.setStyleSheet(
            "background-color:rgb(60, 60, 60); border-radius:0px; border: 1px solid rgba(200, 0, 0, 50);")
        self.shape1.show()
        self.shape1.setGraphicsEffect(shadow)

        self.shape2 = QWidget(self)
        self.shape2.setGeometry(425, 40, 350, 50)
        self.shape2.setStyleSheet(
            "background-color:rgb(120, 0, 0); border-radius:0px; border: 1px solid rgb(50,50,50);")
        self.shape2.show()

        self.header = QLabel("Record Validation", self.shape2)
        self.header.setGeometry(0, 0, 350, 50)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet("""
                                                            QLabel {
                                                                background-color: rgba(200, 200, 0, 0);
                                                                border: 1px solid rgba(0,0,0,0);
                                                                color: rgb(200, 200, 200);
                                                                font-family: Poppins;
                                                                font-size: 20px;
                                                                font-weight: bold;
                                                                }""")

        self.shape_content = self.shape1

        self.readonly_style = """
            QLineEdit {
                background-color: rgb(50, 50, 50);
                border: 1px solid rgba(150, 150, 150, 0);
                border-radius: 0px;
                padding: 5px 12px;
                color: rgb(225, 225, 225);
                font-family: Poppins;
                font-size: 14px;
                }
            QLineEdit:focus {
                border: 1px solid rgba(200, 200, 200, 0);
                background-color: rgb(50, 50, 50);
                }"""

        # Section labels
        label_style = """
                    QLabel {
                        background-color: rgba(152, 152, 152, 0);
                        border: 1px solid rgba(0,0,0,0);
                        color: rgb(200, 200, 200);
                        font-family: Poppins;
                        font-size: 16px;
                        font-weight: regular;
                        }"""

        self.label1 = QLabel("Student Information", self)
        self.label1.setGeometry(175, 90, 250, 20)
        self.label1.setStyleSheet(label_style)

        self.lrn_label = QLabel("LRN", self)
        self.lrn_label.setGeometry(185, 110, 200, 15)
        self.lrn_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.lrn = QLineEdit(self)
        self.lrn.setReadOnly(True)
        self.lrn.setStyleSheet(self.readonly_style)
        self.lrn.setGeometry(175, 125, 200, 30)

        self.first_name_label = QLabel("First Name", self)
        self.first_name_label.setGeometry(185, 170, 200, 15)
        self.first_name_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.first_name = QLineEdit(self)
        self.first_name.setReadOnly(True)
        self.first_name.setStyleSheet(self.readonly_style)
        self.first_name.setGeometry(175, 185, 200, 30)

        self.middle_name_label = QLabel("Middle Name", self)
        self.middle_name_label.setGeometry(400, 170, 200, 15)
        self.middle_name_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.middle_name = QLineEdit(self)
        self.middle_name.setReadOnly(True)
        self.middle_name.setStyleSheet(self.readonly_style)
        self.middle_name.setGeometry(390, 185, 200, 30)

        self.last_name_label = QLabel("Last Name", self)
        self.last_name_label.setGeometry(615, 170, 200, 15)
        self.last_name_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.last_name = QLineEdit(self)
        self.last_name.setReadOnly(True)
        self.last_name.setStyleSheet(self.readonly_style)
        self.last_name.setGeometry(605, 185, 200, 30)

        self.suffix_label = QLabel("Suffix", self)
        self.suffix_label.setGeometry(845, 170, 200, 15)
        self.suffix_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.suffix = QLineEdit(self)
        self.suffix.setReadOnly(True)
        self.suffix.setStyleSheet(self.readonly_style)
        self.suffix.setGeometry(835, 185, 200, 30)

        self.gender_label = QLabel("Gender", self)
        self.gender_label.setGeometry(185, 230, 200, 15)
        self.gender_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.gender = QLineEdit(self)
        self.gender.setReadOnly(True)
        self.gender.setStyleSheet(self.readonly_style)
        self.gender.setGeometry(175, 245, 200, 30)

        self.birthdate_label = QLabel("Birthdate", self)
        self.birthdate_label.setGeometry(400, 230, 200, 15)
        self.birthdate_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.birthdate = QLineEdit(self)
        self.birthdate.setReadOnly(True)
        self.birthdate.setStyleSheet(self.readonly_style)
        self.birthdate.setGeometry(390, 245, 200, 30)

        self.age_label = QLabel("Age", self)
        self.age_label.setGeometry(615, 230, 200, 15)
        self.age_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.age = QLineEdit(self)
        self.age.setReadOnly(True)
        self.age.setStyleSheet(self.readonly_style)
        self.age.setGeometry(605, 245, 200, 30)

        self.nationality_label = QLabel("Nationality", self)
        self.nationality_label.setGeometry(845, 230, 200, 15)
        self.nationality_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.nationality = QLineEdit(self)
        self.nationality.setReadOnly(True)
        self.nationality.setStyleSheet(self.readonly_style)
        self.nationality.setGeometry(835, 245, 200, 30)

        self.religion_label = QLabel("Religion", self)
        self.religion_label.setGeometry(185, 290, 200, 15)
        self.religion_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.religion = QLineEdit(self)
        self.religion.setReadOnly(True)
        self.religion.setStyleSheet(self.readonly_style)
        self.religion.setGeometry(175, 305, 200, 30)

        self.civil_status_label = QLabel("Civil Status", self)
        self.civil_status_label.setGeometry(400, 290, 200, 15)
        self.civil_status_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.civil_status = QLineEdit(self)
        self.civil_status.setReadOnly(True)
        self.civil_status.setStyleSheet(self.readonly_style)
        self.civil_status.setGeometry(390, 305, 200, 30)

        self.contact_number_label = QLabel("Contact Number", self)
        self.contact_number_label.setGeometry(615, 290, 200, 15)
        self.contact_number_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.contact_number = QLineEdit(self)
        self.contact_number.setReadOnly(True)
        self.contact_number.setStyleSheet(self.readonly_style)
        self.contact_number.setGeometry(605, 305, 200, 30)

        self.email_label = QLabel("Email", self)
        self.email_label.setGeometry(845, 290, 200, 15)
        self.email_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.email = QLineEdit(self)
        self.email.setReadOnly(True)
        self.email.setStyleSheet(self.readonly_style)
        self.email.setGeometry(835, 305, 200, 30)

        self.house_label = QLabel("House No. / Street", self)
        self.house_label.setGeometry(185, 350, 415, 15)
        self.house_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.house = QLineEdit(self)
        self.house.setReadOnly(True)
        self.house.setStyleSheet(self.readonly_style)
        self.house.setGeometry(175, 365, 415, 30)

        self.barangay_label = QLabel("Barangay", self)
        self.barangay_label.setGeometry(615, 350, 200, 15)
        self.barangay_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.barangay = QLineEdit(self)
        self.barangay.setReadOnly(True)
        self.barangay.setStyleSheet(self.readonly_style)
        self.barangay.setGeometry(605, 365, 200, 30)

        self.city_label = QLabel("City / Municipality", self)
        self.city_label.setGeometry(845, 350, 200, 15)
        self.city_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.city = QLineEdit(self)
        self.city.setReadOnly(True)
        self.city.setStyleSheet(self.readonly_style)
        self.city.setGeometry(835, 365, 200, 30)

        self.province_label = QLabel("Province", self)
        self.province_label.setGeometry(185, 410, 200, 15)
        self.province_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.province = QLineEdit(self)
        self.province.setReadOnly(True)
        self.province.setStyleSheet(self.readonly_style)
        self.province.setGeometry(175, 425, 200, 30)

        self.zip_label = QLabel("ZIP / Postal Code", self)
        self.zip_label.setGeometry(400, 410, 200, 15)
        self.zip_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.zip = QLineEdit(self)
        self.zip.setReadOnly(True)
        self.zip.setStyleSheet(self.readonly_style)
        self.zip.setGeometry(390, 425, 200, 30)

        self.pg_name_label = QLabel("Parent / Guardian Name", self)
        self.pg_name_label.setGeometry(185, 530, 415, 15)
        self.pg_name_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.pg_name = QLineEdit(self)
        self.pg_name.setReadOnly(True)
        self.pg_name.setStyleSheet(self.readonly_style)
        self.pg_name.setGeometry(175, 545, 415, 30)

        self.relationship_label = QLabel("Relationship", self)
        self.relationship_label.setGeometry(615, 530, 200, 15)
        self.relationship_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.relationship = QLineEdit(self)
        self.relationship.setReadOnly(True)
        self.relationship.setStyleSheet(self.readonly_style)
        self.relationship.setGeometry(605, 545, 200, 30)

        self.occupation_label = QLabel("Occupation", self)
        self.occupation_label.setGeometry(845, 530, 200, 15)
        self.occupation_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.occupation = QLineEdit(self)
        self.occupation.setReadOnly(True)
        self.occupation.setStyleSheet(self.readonly_style)
        self.occupation.setGeometry(835, 545, 200, 30)

        self.pg_contact_label = QLabel("Contact Number", self)
        self.pg_contact_label.setGeometry(185, 590, 200, 15)
        self.pg_contact_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.pg_contact = QLineEdit(self)
        self.pg_contact.setReadOnly(True)
        self.pg_contact.setStyleSheet(self.readonly_style)
        self.pg_contact.setGeometry(175, 605, 200, 30)

        self.pg_address_label = QLabel("Address", self)
        self.pg_address_label.setGeometry(400, 590, 645, 15)
        self.pg_address_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.pg_address = QLineEdit(self)
        self.pg_address.setReadOnly(True)
        self.pg_address.setStyleSheet(self.readonly_style)
        self.pg_address.setGeometry(390, 605, 645, 30)

        self.grade_level_label = QLabel("Grade Level", self)
        self.grade_level_label.setGeometry(185, 470, 200, 15)
        self.grade_level_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0); }")
        self.grade_level = QLineEdit(self)
        self.grade_level.setReadOnly(True)
        self.grade_level.setStyleSheet(self.readonly_style)
        self.grade_level.setGeometry(175, 485, 200, 30)

        self.track_label = QLabel("Track", self)
        self.track_label.setGeometry(400, 470, 200, 15)
        self.track_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.track = QLineEdit(self)
        self.track.setReadOnly(True)
        self.track.setStyleSheet(self.readonly_style)
        self.track.setGeometry(390, 485, 200, 30)

        self.strand_label = QLabel("Strand", self)
        self.strand_label.setGeometry(615, 470, 200, 15)
        self.strand_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.strand = QLineEdit(self)
        self.strand.setReadOnly(True)
        self.strand.setStyleSheet(self.readonly_style)
        self.strand.setGeometry(605, 485, 200, 30)

        self.school_year_label = QLabel("School Year", self)
        self.school_year_label.setGeometry(845, 470, 200, 15)
        self.school_year_label.setStyleSheet("QLabel { color: rgb(180, 180, 180); font-family: Poppins; font-size: 11px; background-color: rgba(180, 180, 180, 0);}")
        self.school_year = QLineEdit(self)
        self.school_year.setReadOnly(True)
        self.school_year.setStyleSheet(self.readonly_style)
        self.school_year.setGeometry(835, 485, 200, 30)

        self.form137 = QPushButton(self)
        self.form137.setText("[Form 137]")
        self.form137.setGeometry(175, 660, 200, 30)
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

        self.birth_certificate = QPushButton(self)
        self.birth_certificate.setText("[Birth Certificate]")
        self.birth_certificate.setGeometry(390, 660, 200, 30)
        self.birth_certificate.setStyleSheet(self.form137.styleSheet())

        self.report_card = QPushButton(self)
        self.report_card.setText("[Report Card]")
        self.report_card.setGeometry(605, 660, 200, 30)
        self.report_card.setStyleSheet(self.form137.styleSheet())

        self.good_moral = QPushButton(self)
        self.good_moral.setText("[Good Moral]")
        self.good_moral.setGeometry(835, 660, 200, 30)
        self.good_moral.setStyleSheet(self.form137.styleSheet())

        # Store document paths
        self.document_paths = {}

        # Connect document buttons
        self.form137.clicked.connect(lambda: self.open_document("Form 137"))
        self.birth_certificate.clicked.connect(lambda: self.open_document("Birth Certificate"))
        self.report_card.clicked.connect(lambda: self.open_document("Report Card"))
        self.good_moral.clicked.connect(lambda: self.open_document("Good Moral"))

        

        # Buttons
        self.back_button = QPushButton(self)
        self.back_button.setText("BACK")
        self.back_button.setGeometry(25, 25, 125, 30)
        self.back_button.setStyleSheet("""
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
                                        border: 1px solid rgb(255, 255, 255);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(50, 50, 50);
                                        border: 2px solid rgb(255, 255, 255);
                                        }""")

        self.reject_button = QPushButton(self)
        self.reject_button.setText("REJECT")
        self.reject_button.setGeometry(875, 735, 100, 40)
        self.reject_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgba(150, 0, 0, 100);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(255, 0, 0, 100);
                                        padding: 8px 12px;
                                        font-family: Poppins;
                                        font-size: 14px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgba(200, 0, 0, 150);
                                        border: 1px solid rgb(255, 0, 0);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgba(100, 0, 0, 150);
                                        border: 2px solid rgb(255, 0, 0);
                                        }""")

        self.approve_button = QPushButton(self)
        self.approve_button.setText("APPROVE")
        self.approve_button.setGeometry(1000, 735, 100, 40)
        self.approve_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgba(0, 150, 0, 100);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(0, 255, 0, 100);
                                        padding: 8px 12px;
                                        font-family: Poppins;
                                        font-size: 14px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgba(0, 200, 0, 150);
                                        border: 1px solid rgb(0, 255, 0);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgba(0, 100, 0, 150);
                                        border: 2px solid rgb(0, 255, 0);
                                        }""")

        # Connect buttons
        self.back_button.clicked.connect(self.handle_back)
        self.reject_button.clicked.connect(self.handle_reject)
        self.approve_button.clicked.connect(self.handle_approve)

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

    def load_registration_data(self, registration_id):
        """Load registration data into the form"""
        if not registration_id:
            return

        # Get registration details
        reg_data = self.controller.get_registration_details(registration_id)
        if not reg_data:
            QMessageBox.warning(self, "Error", "Could not load registration data.")
            return

        # Get documents
        documents = self.controller.get_registration_documents(registration_id)
        for doc in documents:
            doc_type = doc.get("DocumentType")
            file_path = doc.get("FilePath")
            if doc_type and file_path:
                self.document_paths[doc_type] = file_path

        # Populate fields
        self.lrn.setText(reg_data.get("LRN") or "")
        self.first_name.setText(reg_data.get("FirstName") or "")
        self.middle_name.setText(reg_data.get("MiddleName") or "")
        self.last_name.setText(reg_data.get("LastName") or "")
        self.suffix.setText("")  # Suffix not in database
        self.gender.setText(reg_data.get("Gender") or "")
        
        birthdate = reg_data.get("Birthdate")
        if birthdate:
            if isinstance(birthdate, str):
                self.birthdate.setText(birthdate)
            else:
                self.birthdate.setText(birthdate.strftime("%Y-%m-%d"))
        else:
            self.birthdate.setText("")

        self.age.setText(str(reg_data.get("Age")) if reg_data.get("Age") else "")
        self.nationality.setText(reg_data.get("Nationality") or "")
        self.religion.setText(reg_data.get("Religion") or "")
        self.civil_status.setText(reg_data.get("CivilStatus") or "")
        self.contact_number.setText(reg_data.get("ContactNum") or "")
        self.email.setText(reg_data.get("Email") or "")

        # Address
        self.house.setText(reg_data.get("HouseNum") or "")
        self.barangay.setText(reg_data.get("Barangay") or "")
        self.city.setText(reg_data.get("City") or "")
        self.province.setText(reg_data.get("Province") or "")
        self.zip.setText(reg_data.get("ZIP") or "")

        # Parent/Guardian
        self.pg_name.setText(reg_data.get("PGName") or "")
        self.relationship.setText(reg_data.get("Relationship") or "")
        self.occupation.setText(reg_data.get("Occupation") or "")
        self.pg_contact.setText(reg_data.get("PGContact") or "")
        self.pg_address.setText(reg_data.get("PGAddress") or "")

        # Academic
        self.grade_level.setText(reg_data.get("GradeLevel") or "")
        self.track.setText(reg_data.get("Track") or "")
        self.strand.setText(reg_data.get("Strand") or "")
        self.school_year.setText(reg_data.get("SchoolYear") or "")

        # No registration info fields to populate

    def handle_back(self):
        """Handle back button - return to registrar dashboard"""
        self.main_window.switch_view("registrar_dashboard")

    def handle_reject(self):
        """Handle reject button"""
        registration_id = getattr(self.main_window, 'selected_registration_id', None)
        if not registration_id:
            QMessageBox.warning(self, "Error", "No registration selected.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Rejection",
            "Are you sure you want to reject this registration?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            validated_by = self.main_window.current_user.get("account_id") if self.main_window.current_user else None
            if not validated_by:
                QMessageBox.critical(self, "Error", "No user session found. Please log in again.")
                return
            if self.controller.validate_registration(registration_id, "Rejected", validated_by):
                QMessageBox.information(self, "Success", "Registration rejected successfully.")
                self.handle_back()
            else:
                QMessageBox.critical(self, "Error", "Failed to reject registration. Please ensure you have a valid employee account.")

    def handle_approve(self):
        """Handle approve button"""
        registration_id = getattr(self.main_window, 'selected_registration_id', None)
        if not registration_id:
            QMessageBox.warning(self, "Error", "No registration selected.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Approval",
            "Are you sure you want to approve this registration?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            validated_by = self.main_window.current_user.get("account_id") if self.main_window.current_user else None
            if not validated_by:
                QMessageBox.critical(self, "Error", "No user session found. Please log in again.")
                return
            if self.controller.validate_registration(registration_id, "Approved", validated_by):
                QMessageBox.information(self, "Success", "Registration approved successfully.")
                self.handle_back()
            else:
                QMessageBox.critical(self, "Error", "Failed to approve registration. Please ensure you have a valid employee account.")
