from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, \
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QScrollArea, QComboBox, QDateEdit, QFileDialog
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QRect, QDate
import os

class AccountRecoverySecurity(QWidget):
    def __init__(self, main_window, controller):
        super().__init__()
        self.main_window = main_window
        self.controller = controller
        self.setWindowTitle("SHS Registration System")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background-color:rgb(50, 50, 50);")

        # --- LOGO ---
        self.logo = QLabel(self)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files", "Final Logo - White.png")
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaled(150, 45, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setGeometry(525, 25, 150, 45)

        # --- 400x400 MAIN SHAPE (centered) ---
        self.shape_main = QWidget(self)
        self.shape_main.setGeometry(400, 200, 400, 400)
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

        # Title: RECOVERY
        self.title_label = QLabel("RECOVERY", self)
        self.title_label.setGeometry(500, 225, 200, 50)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 32px;
                font-weight: bold;
            }
        """)

        # Security question label (will be updated with actual question)
        self.question_label = QLabel("Enter your username", self)
        self.question_label.setGeometry(450, 300, 300, 20)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 12px;
                font-weight: normal;
            }
        """)

        # Security answer label
        self.label_answer = QLabel("Security Answer", self)
        self.label_answer.setGeometry(460, 345, 100, 15)
        self.label_answer.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 12px;
                font-weight: normal;
            }
        """)

        # Security answer input
        self.answer_input = QLineEdit(self)
        self.answer_input.setGeometry(450, 360, 300, 50)
        self.answer_input.setStyleSheet("""
            QLineEdit {
                background-color: rgb(50, 50, 50);
                border-radius: 0px;
                border: 1px solid rgb(132, 132, 132);
                padding: 10px 12px;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 14px;
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
        """)

        # Primary button: VERIFY ANSWER
        self.submit = QPushButton("VERIFY ANSWER", self)
        self.submit.setGeometry(450, 440, 300, 50)
        self.submit.setStyleSheet("""
            QPushButton {
                background-color: rgb(193, 193, 193);
                color: rgb(50, 50, 50);
                border-radius: 0px;
                border: 1px solid rgb(132, 132, 132);
                padding: 10px 12px;
                font-family: Poppins;
                font-size: 20px;
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
        """)

        # Back to Login button
        self.back = QPushButton("BACK TO LOGIN", self)
        self.back.setGeometry(450, 510, 300, 50)
        self.back.setStyleSheet("""
            QPushButton {
                background-color: rgba(60, 60, 60, 0);
                color: rgb(234, 234, 234);
                border-radius: 0px;
                border: 1px solid rgb(193, 193, 193);
                padding: 10px 12px;
                font-family: Poppins;
                font-size: 16px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: rgb(70, 70, 70);
            }
            QPushButton:pressed {
                background-color: rgb(40, 40, 40);
            }
        """)

        # Connect buttons
        self.submit.clicked.connect(self.handle_verify)
        self.back.clicked.connect(self.handle_back)

    def load_security_question(self):
        """Load and display security question"""
        if self.main_window.recovery_account_id:
            account = self.controller.account_model.get_account_by_id(self.main_window.recovery_account_id)
            if account and account.get("SecurityQuestion"):
                self.question_label.setText(account['SecurityQuestion'])
            else:
                self.question_label.setText("No security question set for this account.")

    def handle_verify(self):
        """Verify security answer"""
        if not self.main_window.recovery_account_id:
            QMessageBox.warning(self, "Error", "No account selected.")
            return

        answer = self.answer_input.text().strip()
        if not answer:
            QMessageBox.warning(self, "Error", "Please enter your security answer.")
            return

        if self.controller.verify_security_answer(self.main_window.recovery_account_id, answer):
            self.main_window.switch_view("account_recovery_reset")
        else:
            QMessageBox.warning(self, "Error", "Incorrect security answer.")

    def handle_back(self):
        """Handle back button"""
        self.main_window.switch_view("account_recovery")
