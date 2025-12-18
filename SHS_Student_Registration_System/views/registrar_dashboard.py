from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, \
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QScrollArea, QComboBox, QDateEdit, QFileDialog, QTableWidget, \
    QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QRect, QDate
import os

class RegistrarDashboard(QWidget):
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
        self.shape1.setGeometry(25, 100, 1150, 600)
        self.shape1.setStyleSheet(
            "background-color:rgb(60, 60, 60); border-radius:0px; border: 1px solid rgba(200, 0, 0, 50);")
        self.shape1.show()
        self.shape1.setGraphicsEffect(shadow)

        self.shape2 = QWidget(self)
        self.shape2.setGeometry(425, 75, 350, 50)
        self.shape2.setStyleSheet(
            "background-color:rgb(120, 0, 0); border-radius:0px; border: 1px solid rgb(50,50,50);")
        self.shape2.show()

        self.header = QLabel("Registrar Dashboard", self.shape2)
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

        # Filters
        filter_y = 120
        self.filter_label = QLabel("Filter:", self.shape1)
        self.filter_label.setGeometry(25, filter_y, 50, 35)
        self.filter_label.setStyleSheet("""
                                    QLabel {
                                        background-color: rgba(0, 0, 0, 0);
                                        border: none;
                                        color: rgb(200, 200, 200);
                                        font-family: Poppins;
                                        font-size: 14px;
                                        }""")
        
        self.search_bar = QLineEdit(self.shape1)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setStyleSheet("""
                                    QLineEdit {
                                    background-color: rgb(50, 50, 50);
                                    border: 1px solid rgba(150, 150, 150, 0);
                                    border-radius: 0px;
                                    padding: 8px 12px;
                                    color: rgb(225, 225, 225);
                                    font-family: Poppins;
                                    font-size: 14px;
                                    }
                                    QLineEdit:focus {
                                    border: 1px solid rgba(200, 200, 200, 255);
                                    background-color: rgb(50, 50, 50);
                                    }""")
        self.search_bar.setGeometry(85, filter_y, 200, 35)
        self.search_bar.textChanged.connect(self.apply_filters)

        self.grade_filter = QComboBox(self.shape1)
        self.grade_filter.addItems(["ALL", "Grade 11", "Grade 12"])
        self.grade_filter.setStyleSheet("""
                                QComboBox {
                                    padding-left: 10px;
                                    padding-top: 5px;
                                    padding-bottom: 5px;
                                    border: 1px solid rgb(152, 152, 152);
                                    border-radius: 0px;
                                    color: rgb(200, 200, 200);
                                    background-color: rgb(50, 50, 50);
                                    font-family: Poppins;
                                    font-size: 12px;
                                    }
                                QComboBox::drop-down {
                                    width: 30px;
                                    border-radius: 0px;
                                    border-top-left-radius: 0px;
                                    border-bottom-left-radius: 0px;
                                    border: 1px solid rgba(255, 255, 255, 100);
                                    background-color: rgb(70, 70, 70);
                                    }
                                QComboBox QAbstractItemView {
                                    background-color: rgb(50, 50, 50);
                                    color: rgb(200, 200, 200);
                                    selection-background-color: rgb(100, 100, 100);
                                    }""")
        self.grade_filter.setGeometry(300, filter_y, 120, 35)
        self.grade_filter.currentTextChanged.connect(self.apply_filters)

        self.track_filter = QComboBox(self.shape1)
        self.track_filter.addItems(["ALL", "Academic", "TVL"])
        self.track_filter.setStyleSheet(self.grade_filter.styleSheet())
        self.track_filter.setGeometry(430, filter_y, 120, 35)
        self.track_filter.currentTextChanged.connect(self.apply_filters)

        self.strand_filter = QComboBox(self.shape1)
        self.strand_filter.addItems(["ALL", "STEM", "HUMSS", "ABM", "GAS", "ICT", "HE", "IA"])
        self.strand_filter.setStyleSheet(self.grade_filter.styleSheet())
        self.strand_filter.setGeometry(560, filter_y, 120, 35)
        self.strand_filter.currentTextChanged.connect(self.apply_filters)

        self.status_filter = QComboBox(self.shape1)
        self.status_filter.addItems(["ALL", "Pending", "Approved", "Rejected"])
        self.status_filter.setStyleSheet(self.grade_filter.styleSheet())
        self.status_filter.setGeometry(690, filter_y, 120, 35)
        self.status_filter.currentTextChanged.connect(self.apply_filters)

        # Table
        self.table = QTableWidget(self.shape1)
        self.table.setGeometry(25, filter_y + 50, 1100, 400)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Registration ID", "LRN", "Full Name", "Grade Level", "Track", "Strand", "Status"])
        self.table.verticalHeader().setDefaultSectionSize(45)  # Set row height to 45
        self.table.horizontalHeader().setStyleSheet("""
                                    QHeaderView::section {
                                        background-color: rgb(70, 70, 70);
                                        color: rgb(200, 200, 200);
                                        padding: 8px;
                                        border: 1px solid rgb(50, 50, 50);
                                        font-family: Poppins;
                                        font-weight: bold;
                                        }""")
        self.table.setStyleSheet("""
                                    QTableWidget {
                                        background-color: rgb(50, 50, 50);
                                        color: rgb(200, 200, 200);
                                        border: 1px solid rgb(100, 100, 100);
                                        border-radius: 0px;
                                        gridline-color: rgb(70, 70, 70);
                                        font-family: Poppins;
                                        }
                                    QTableWidget::item {
                                        padding: 5px;
                                        }
                                    QTableWidget::item:selected {
                                        background-color: rgb(120, 120, 120);
                                        }
                                    QTableWidget::item:hover {
                                        background-color: rgb(100, 100, 100);
                                        }""")
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.handle_row_double_click)
        
        # Set initial column widths (approximately 150px each, with Full Name stretching)
        self.table.setColumnWidth(0, 150)  # Registration ID
        self.table.setColumnWidth(1, 150)  # LRN
        # Full Name will stretch
        self.table.setColumnWidth(3, 150)  # Grade Level
        self.table.setColumnWidth(4, 150)  # Track
        self.table.setColumnWidth(5, 150)  # Strand
        self.table.setColumnWidth(6, 150)  # Status

        # View button
        self.view_button = QPushButton(self.shape1)
        self.view_button.setText("Open")
        self.view_button.setGeometry(1000, filter_y, 100, 35)
        self.view_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(150, 150, 150);
                                        color: rgb(50, 50, 50);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 0);
                                        padding: 8px 12px;
                                        font-family: Poppins;
                                        font-size: 14px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(175, 175, 175);
                                        border: 1px solid rgb(255, 255, 255);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(125, 125, 125);
                                        border: 2px solid rgb(255, 255, 255);
                                        }""")
        self.view_button.clicked.connect(self.handle_view_selected)

        # Store all records
        self.all_records = []

        # Load data
        self.load_registration_records()

        # Connect logout button
        self.logout.clicked.connect(self.handle_logout)

        self.setLayout(layout)

    def load_registration_records(self):
        """Load all registration records"""
        self.all_records = self.controller.get_all_registration_records()
        self.apply_filters()

    def apply_filters(self):
        """Apply filters and search to the table"""
        # Get filter values
        search_text = self.search_bar.text().lower()
        grade_filter = self.grade_filter.currentText()
        track_filter = self.track_filter.currentText()
        strand_filter = self.strand_filter.currentText()
        status_filter = self.status_filter.currentText()

        # Filter records
        filtered_records = []
        for record in self.all_records:
            # Search filter
            if search_text:
                searchable = f"{record.get('RegistrationID', '')} {record.get('LRN', '')} {record.get('FirstName', '')} {record.get('LastName', '')}".lower()
                if search_text not in searchable:
                    continue

            # Grade filter
            if grade_filter != "ALL" and record.get("GradeLevel") != grade_filter:
                continue

            # Track filter
            if track_filter != "ALL" and record.get("Track") != track_filter:
                continue

            # Strand filter
            if strand_filter != "ALL" and record.get("Strand") != strand_filter:
                continue

            # Status filter
            if status_filter != "ALL" and record.get("Status") != status_filter:
                continue

            filtered_records.append(record)

        # Populate table
        self.table.setRowCount(len(filtered_records))
        for row, record in enumerate(filtered_records):
            # Registration ID
            self.table.setItem(row, 0, QTableWidgetItem(record.get("RegistrationID", "N/A")))

            # LRN
            self.table.setItem(row, 1, QTableWidgetItem(record.get("LRN") or "N/A"))

            # Full Name (last_name, first_name)
            first_name = record.get("FirstName") or ""
            last_name = record.get("LastName") or ""
            full_name = f"{last_name}, {first_name}" if last_name and first_name else (last_name or first_name or "N/A")
            self.table.setItem(row, 2, QTableWidgetItem(full_name))

            # Grade Level
            self.table.setItem(row, 3, QTableWidgetItem(record.get("GradeLevel") or "N/A"))

            # Track
            self.table.setItem(row, 4, QTableWidgetItem(record.get("Track") or "N/A"))

            # Strand
            self.table.setItem(row, 5, QTableWidgetItem(record.get("Strand") or "N/A"))

            # Status
            status_item = QTableWidgetItem(record.get("Status") or "N/A")
            status = record.get("Status", "")
            if status == "Approved":
                status_item.setForeground(QColor(0, 255, 0))
            elif status == "Rejected":
                status_item.setForeground(QColor(255, 0, 0))
            elif status == "Pending":
                status_item.setForeground(QColor(255, 255, 0))
            self.table.setItem(row, 6, status_item)

        # Resize columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Registration ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # LRN
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Full Name stretches
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Grade Level
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Track
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Strand
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Status

    def handle_row_double_click(self, index):
        """Handle double-click on table row"""
        self.open_registration_validation(index.row())

    def handle_view_selected(self):
        """Handle view button click"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.open_registration_validation(current_row)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a record to view.")

    def open_registration_validation(self, row):
        """Open registration validation view for selected record"""
        registration_id_item = self.table.item(row, 0)
        if registration_id_item:
            registration_id = registration_id_item.text()
            # Store selected registration ID for validation view
            self.main_window.selected_registration_id = registration_id
            self.main_window.switch_view("registrar_validation")

    def handle_logout(self):
        """Handle logout button click"""
        self.main_window.current_user = None
        self.main_window.switch_view("login")
