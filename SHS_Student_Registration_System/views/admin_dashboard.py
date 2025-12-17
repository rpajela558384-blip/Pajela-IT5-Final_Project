from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, \
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QScrollArea, QComboBox, QDateEdit, QFileDialog, QTableWidget, \
    QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QRect, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import datetime

class AdminDashboard(QWidget):
    def __init__(self, main_window, controller):
        super().__init__()
        self.main_window = main_window
        self.controller = controller
        self.current_view = "reports"
        self.selected_account_id = None
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
        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(10)
        shadow1.setXOffset(10)
        shadow1.setYOffset(10)
        shadow1.setColor(QColor(0, 0, 0, 160))

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(10)
        shadow2.setXOffset(10)
        shadow2.setYOffset(10)
        shadow2.setColor(QColor(0, 0, 0, 160))

        shadow3 = QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(10)
        shadow3.setXOffset(10)
        shadow3.setYOffset(10)
        shadow3.setColor(QColor(0, 0, 0, 160))

        # Shape1 - Main content area
        self.shape1 = QWidget(self)
        self.shape1.setGeometry(175, 70, 850, 400)
        self.shape1.setStyleSheet(
            "background-color:rgb(60, 60, 60); border-radius:0px; border: 1px solid rgba(200, 0, 0, 50);")
        self.shape1.show()
        self.shape1.setGraphicsEffect(shadow1)
        self.shape1.update()

        # Shape2 - Header
        self.shape2 = QWidget(self)
        self.shape2.setGeometry(425, 40, 350, 50)
        self.shape2.setStyleSheet(
            "background-color:rgb(120, 0, 0); border-radius:0px; border: 1px solid rgb(50,50,50);")
        self.shape2.show()

        # Shape3 - Secondary content (graph or CRUD)
        self.shape3 = QWidget(self)
        self.shape3.setGeometry(175, 495, 500, 250)
        self.shape3.setStyleSheet(
            "background-color:rgb(60, 60, 60); border-radius:0px; border: 1px solid rgba(200, 0, 0, 50);")
        self.shape3.show()
        self.shape3.setGraphicsEffect(shadow2)
        self.shape3.update()
        
        # Scroll area for shape3 content (for accounts CRUD)
        self.shape3_scroll = QScrollArea(self.shape3)
        self.shape3_scroll.setGeometry(10, 10, 480, 230)
        self.shape3_scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: rgb(50, 50, 50);
                width: 10px;
                                    border-radius: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: rgb(100, 100, 100);
                                    border-radius: 0px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgb(120, 120, 120);
            }
        """)
        self.shape3_scroll.setWidgetResizable(True)
        self.shape3_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.shape3_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.shape3_scroll.hide()  # Initially hidden (starts with reports view)
        
        # Content widget for shape3 scroll area
        self.shape3_content = QWidget()
        self.shape3_content.setStyleSheet("background-color: transparent;")
        self.shape3_content.setMinimumHeight(300)  # Enough height for all fields
        self.shape3_scroll.setWidget(self.shape3_content)

        # Shape4 - Buttons (REPORTS/ACCOUNTS)
        self.shape4 = QWidget(self)
        self.shape4.setGeometry(725, 495, 300, 250)
        self.shape4.setStyleSheet(
            "background-color:rgb(60, 60, 60); border-radius:0px; border: 1px solid rgba(200, 0, 0, 50);")
        self.shape4.setGraphicsEffect(shadow3)
        self.shape4.show()

        # Header
        self.header = QLabel("Admin Dashboard", self.shape2)
        self.header.setGeometry(75, 10, 250, 30)
        self.header.setStyleSheet("""
                                    QLabel {
                                        background-color: rgba(200, 200, 0, 0);
                                        border: 1px solid rgba(0,0,0,0);
                                        color: rgb(200, 200, 200);
                                        font-family: Poppins;
                                        font-size: 20px;
                                        font-weight: bold;
                                        }""")

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
        self.logout.clicked.connect(self.handle_logout)

        # View toggle buttons in shape4
        self.reports_btn = QPushButton("REPORTS", self.shape4)
        self.reports_btn.setGeometry(25, 25, 250, 50)
        self.reports_btn.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(120, 0, 0);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 0);
                                        padding: 8px 12px;
                                        font-family: Poppins;
                                        font-size: 16px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(150, 0, 0);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(100, 0, 0);
                                        }""")
        self.reports_btn.clicked.connect(lambda: self.switch_view("reports"))

        self.accounts_btn = QPushButton("ACCOUNTS", self.shape4)
        self.accounts_btn.setGeometry(25, 90, 250, 50)
        self.accounts_btn.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(60, 60, 60);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 0);
                                        padding: 8px 12px;
                                        font-family: Poppins;
                                        font-size: 16px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(80, 80, 80);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(50, 50, 50);
                                        }""")
        self.accounts_btn.clicked.connect(lambda: self.switch_view("accounts"))

        # Initialize REPORTS view components
        self.init_reports_view()
        # Initialize ACCOUNTS view components
        self.init_accounts_view()

        # Show initial view
        self.switch_view("reports")

        self.setLayout(layout)

    def init_reports_view(self):
        """Initialize REPORTS view components"""
        # Statistics cards (horizontal, small)
        card_width = 180
        card_height = 60
        card_y = 25
        card_spacing = 20
        start_x = 25

        # Registered card
        self.registered_card = QWidget(self.shape1)
        self.registered_card.setGeometry(start_x, card_y, card_width, card_height)
        self.registered_card.setStyleSheet("background-color: rgb(50, 50, 50); border-radius: 0px; border: 1px solid rgba(150, 150, 150, 100);")
        
        self.registered_label = QLabel("Registered", self.registered_card)
        self.registered_label.setGeometry(10, 5, 160, 20)
        self.registered_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.registered_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")
        
        self.registered_value = QLabel("0", self.registered_card)
        self.registered_value.setGeometry(10, 25, 160, 30)
        self.registered_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.registered_value.setStyleSheet("color: rgb(225, 225, 225); font-family: Poppins; font-size: 20px; font-weight: bold; background-color: transparent; border: none;")

        # Pending card
        self.pending_card = QWidget(self.shape1)
        self.pending_card.setGeometry(start_x + card_width + card_spacing, card_y, card_width, card_height)
        self.pending_card.setStyleSheet("background-color: rgba(180, 180, 0, 50); border-radius: 0px; border: 1px solid rgba(255, 255, 0, 100);")
        
        self.pending_label = QLabel("Pending", self.pending_card)
        self.pending_label.setGeometry(10, 5, 160, 20)
        self.pending_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.pending_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")
        
        self.pending_value = QLabel("0", self.pending_card)
        self.pending_value.setGeometry(10, 25, 160, 30)
        self.pending_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.pending_value.setStyleSheet("color: rgb(225, 225, 225); font-family: Poppins; font-size: 20px; font-weight: bold; background-color: transparent; border: none;")

        # Approved card
        self.approved_card = QWidget(self.shape1)
        self.approved_card.setGeometry(start_x + (card_width + card_spacing) * 2, card_y, card_width, card_height)
        self.approved_card.setStyleSheet("background-color: rgba(0, 180, 0, 50); border-radius: 0px; border: 1px solid rgba(0, 255, 0, 100);")
        
        self.approved_label = QLabel("Approved", self.approved_card)
        self.approved_label.setGeometry(10, 5, 160, 20)
        self.approved_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.approved_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")
        
        self.approved_value = QLabel("0", self.approved_card)
        self.approved_value.setGeometry(10, 25, 160, 30)
        self.approved_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.approved_value.setStyleSheet("color: rgb(225, 225, 225); font-family: Poppins; font-size: 20px; font-weight: bold; background-color: transparent; border: none;")

        # Rejected card
        self.rejected_card = QWidget(self.shape1)
        self.rejected_card.setGeometry(start_x + (card_width + card_spacing) * 3, card_y, card_width, card_height)
        self.rejected_card.setStyleSheet("background-color: rgba(180, 0, 0, 50); border-radius: 0px; border: 1px solid rgba(255, 0, 0, 100);")
        
        self.rejected_label = QLabel("Rejected", self.rejected_card)
        self.rejected_label.setGeometry(10, 5, 160, 20)
        self.rejected_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.rejected_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")
        
        self.rejected_value = QLabel("0", self.rejected_card)
        self.rejected_value.setGeometry(10, 25, 160, 30)
        self.rejected_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.rejected_value.setStyleSheet("color: rgb(225, 225, 225); font-family: Poppins; font-size: 20px; font-weight: bold; background-color: transparent; border: none;")

        # Filters
        filter_y = card_y + card_height + 20
        self.reports_filter_label = QLabel("Filter:", self.shape1)
        self.reports_filter_label.setGeometry(25, filter_y, 50, 35)
        self.reports_filter_label.setStyleSheet("""
                                    QLabel {
                                        background-color: rgba(0, 0, 0, 0);
                                        border: none;
                                        color: rgb(200, 200, 200);
                                        font-family: Poppins;
                                        font-size: 14px;
                                        }""")
        self.reports_filter_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.reports_search = QLineEdit(self.shape1)
        self.reports_search.setPlaceholderText("Search...")
        self.reports_search.setStyleSheet("""
                                    QLineEdit {
                                    background-color: rgb(50, 50, 50);
                                    border: 1px solid rgba(150, 150, 150, 0);
                                    border-radius: 0px;
                                    padding: 8px 12px;
                                    color: rgb(225, 225, 225);
                                    font-family: Poppins;
                                    font-size: 14px;
                                    }""")
        self.reports_search.setGeometry(85, filter_y, 200, 35)
        self.reports_search.textChanged.connect(self.apply_reports_filters)

        # Date range filters
        self.date_from_label = QLabel("From:", self.shape1)
        self.date_from_label.setGeometry(300, filter_y, 50, 35)
        self.date_from_label.setStyleSheet("""
                                    QLabel {
                                        background-color: rgba(0, 0, 0, 0);
                                        border: none;
                                        color: rgb(200, 200, 200);
                                        font-family: Poppins;
                                        font-size: 12px;
                                        }""")
        self.date_from_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.reports_date_from = QDateEdit(self.shape1)
        self.reports_date_from.setCalendarPopup(True)
        self.reports_date_from.setDate(QDate.currentDate().addYears(-1))
        self.reports_date_from.setStyleSheet("""
                                QDateEdit {
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
                                QDateEdit::drop-down {
                                    width: 30px;
                                    border-radius: 0px;
                                    }""")
        self.reports_date_from.setGeometry(350, filter_y, 120, 35)
        self.reports_date_from.dateChanged.connect(self.apply_reports_filters)

        self.date_to_label = QLabel("To:", self.shape1)
        self.date_to_label.setGeometry(480, filter_y, 30, 35)
        self.date_to_label.setStyleSheet("""
                                    QLabel {
                                        background-color: rgba(0, 0, 0, 0);
                                        border: none;
                                        color: rgb(200, 200, 200);
                                        font-family: Poppins;
                                        font-size: 12px;
                                        }""")
        self.date_to_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.reports_date_to = QDateEdit(self.shape1)
        self.reports_date_to.setCalendarPopup(True)
        self.reports_date_to.setDate(QDate.currentDate())
        self.reports_date_to.setStyleSheet(self.reports_date_from.styleSheet())
        self.reports_date_to.setGeometry(510, filter_y, 120, 35)
        self.reports_date_to.dateChanged.connect(self.apply_reports_filters)

        self.reports_status = QComboBox(self.shape1)
        self.reports_status.addItems(["ALL", "Pending", "Approved", "Rejected"])
        self.reports_status.setStyleSheet("""
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
                                    }""")
        self.reports_status.setGeometry(640, filter_y, 120, 35)
        self.reports_status.currentTextChanged.connect(self.apply_reports_filters)

        # Table
        self.reports_table = QTableWidget(self.shape1)
        self.reports_table.setGeometry(25, filter_y + 45, 800, 200)
        self.reports_table.setColumnCount(5)
        self.reports_table.setHorizontalHeaderLabels(["Registration ID", "Student ID", "Validated By", "Registration Date", "Status"])
        self.reports_table.verticalHeader().setDefaultSectionSize(40)
        self.reports_table.horizontalHeader().setStyleSheet("""
                                    QHeaderView::section {
                                        background-color: rgb(70, 70, 70);
                                        color: rgb(200, 200, 200);
                                        padding: 8px;
                                        border: 1px solid rgb(50, 50, 50);
                                        font-family: Poppins;
                                        font-weight: bold;
                                        }""")
        self.reports_table.setStyleSheet("""
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
                                        background-color: rgb(120, 120, 120);
                                        }""")
        self.reports_table.setAlternatingRowColors(True)
        self.reports_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.reports_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.reports_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.reports_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Statistics labels below table
        stats_y = filter_y + 45 + 200 + 15
        self.stats_registered_label = QLabel("Registered: 0", self.shape1)
        self.stats_registered_label.setGeometry(25, stats_y, 180, 20)
        self.stats_registered_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        self.stats_pending_label = QLabel("Pending: 0", self.shape1)
        self.stats_pending_label.setGeometry(220, stats_y, 180, 20)
        self.stats_pending_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        self.stats_approved_label = QLabel("Approved: 0", self.shape1)
        self.stats_approved_label.setGeometry(415, stats_y, 180, 20)
        self.stats_approved_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        self.stats_rejected_label = QLabel("Rejected: 0", self.shape1)
        self.stats_rejected_label.setGeometry(610, stats_y, 180, 20)
        self.stats_rejected_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        # Graph in shape3 (not in scroll area, directly on shape3)
        self.graph_figure = Figure(figsize=(4, 2))
        self.graph_canvas = FigureCanvas(self.graph_figure)
        self.graph_canvas.setParent(self.shape3)
        self.graph_canvas.setGeometry(10, 10, 480, 230)

        # Store all records
        self.all_registration_records = []

    def init_accounts_view(self):
        """Initialize ACCOUNTS view components"""
        # Filters
        filter_y = 25
        self.accounts_filter_label = QLabel("Filter:", self.shape1)
        self.accounts_filter_label.setGeometry(25, filter_y, 50, 35)
        self.accounts_filter_label.setStyleSheet("""
                                    QLabel {
                                        background-color: rgba(0, 0, 0, 0);
                                        border: none;
                                        color: rgb(200, 200, 200);
                                        font-family: Poppins;
                                        font-size: 14px;
                                        }""")
        self.accounts_filter_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.accounts_search = QLineEdit(self.shape1)
        self.accounts_search.setPlaceholderText("Search...")
        self.accounts_search.setStyleSheet("""
                                    QLineEdit {
                                    background-color: rgb(50, 50, 50);
                                    border: 1px solid rgba(150, 150, 150, 0);
                                    border-radius: 0px;
                                    padding: 8px 12px;
                                    color: rgb(225, 225, 225);
                                    font-family: Poppins;
                                    font-size: 14px;
                                    }""")
        self.accounts_search.setGeometry(85, filter_y, 200, 35)
        self.accounts_search.textChanged.connect(self.apply_accounts_filters)

        self.accounts_role = QComboBox(self.shape1)
        self.accounts_role.addItems(["ALL", "admin", "registrar", "student"])
        self.accounts_role.setStyleSheet("""
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
                                    border-left: 1px solid rgb(152, 152, 152);
                                    background-color: rgb(50, 50, 50);
                                    }
                                QComboBox QAbstractItemView {
                                    background-color: rgb(50, 50, 50);
                                    color: rgb(200, 200, 200);
                                    selection-background-color: rgb(90, 90, 90);
                                    }""")
        self.accounts_role.setGeometry(300, filter_y, 150, 35)
        self.accounts_role.currentTextChanged.connect(self.apply_accounts_filters)

        # Accounts table
        self.accounts_table = QTableWidget(self.shape1)
        self.accounts_table.setGeometry(25, filter_y + 45, 800, 330)
        self.accounts_table.setColumnCount(6)
        self.accounts_table.setHorizontalHeaderLabels(["Account ID", "Username", "UUID", "Password", "Security Question", "Security Answer"])
        self.accounts_table.verticalHeader().setDefaultSectionSize(40)
        self.accounts_table.horizontalHeader().setStyleSheet("""
                                    QHeaderView::section {
                                        background-color: rgb(70, 70, 70);
                                        color: rgb(200, 200, 200);
                                        padding: 8px;
                                        border: 1px solid rgb(50, 50, 50);
                                        font-family: Poppins;
                                        font-weight: bold;
                                        }""")
        self.accounts_table.setStyleSheet("""
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
                                        background-color: rgb(120, 120, 120);
                                        }""")
        self.accounts_table.setAlternatingRowColors(True)
        self.accounts_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.accounts_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.accounts_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.accounts_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.accounts_table.itemSelectionChanged.connect(self.on_account_selected)

        # CRUD in shape3 (using shape3_content for scrollable area)
        crud_y = 20
        # Account name (top, 415w)
        self.account_name_label = QLabel("Account:", self.shape3_content)
        self.account_name_label.setGeometry(20, crud_y, 100, 25)
        self.account_name_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        self.account_name_field = QLineEdit(self.shape3_content)
        self.account_name_field.setReadOnly(True)
        self.account_name_field.setStyleSheet("""
                                    QLineEdit {
                                    background-color: rgb(50, 50, 50);
                                    border: 1px solid rgba(150, 150, 150, 0);
                                    border-radius: 0px;
                                    padding: 5px 12px;
                                    color: rgb(225, 225, 225);
                                    font-family: Poppins;
                                    font-size: 14px;
                                    }""")
        self.account_name_field.setGeometry(20, crud_y + 25, 415, 30)

        # Username and Role (row 2, 200x30 each with 15px spacing)
        self.username_label = QLabel("Username:", self.shape3_content)
        self.username_label.setGeometry(20, crud_y + 65, 100, 25)
        self.username_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        self.username_field = QLineEdit(self.shape3_content)
        self.username_field.setStyleSheet("""
                                    QLineEdit {
                                    background-color: rgb(50, 50, 50);
                                    border: 1px solid rgba(150, 150, 150, 0);
                                    border-radius: 0px;
                                    padding: 5px 12px;
                                    color: rgb(225, 225, 225);
                                    font-family: Poppins;
                                    font-size: 14px;
                                    }""")
        self.username_field.setGeometry(20, crud_y + 90, 200, 30)

        self.role_label = QLabel("Role:", self.shape3_content)
        self.role_label.setGeometry(235, crud_y + 65, 100, 25)
        self.role_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        self.role_field = QComboBox(self.shape3_content)
        self.role_field.addItems(["admin", "registrar"])
        self.role_field.setStyleSheet("""
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
                                    border-left: 1px solid rgb(152, 152, 152);
                                    background-color: rgb(50, 50, 50);
                                    }
                                QComboBox QAbstractItemView {
                                    background-color: rgb(50, 50, 50);
                                    color: rgb(200, 200, 200);
                                    selection-background-color: rgb(90, 90, 90);
                                    }""")
        self.role_field.setGeometry(235, crud_y + 90, 200, 30)

        # Security Question and Security Answer (row 3, 200x30 each)
        self.security_question_label = QLabel("Security Question:", self.shape3_content)
        self.security_question_label.setGeometry(20, crud_y + 125, 150, 25)
        self.security_question_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        self.security_question_field = QComboBox(self.shape3_content)
        self.security_question_field.addItems(["What is your favorite color?", "What is your favorite food?", "What is your favorite animal?"])
        self.security_question_field.setStyleSheet("""
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
                                    }""")
        self.security_question_field.setGeometry(20, crud_y + 150, 200, 30)

        self.security_answer_label = QLabel("Security Answer:", self.shape3_content)
        self.security_answer_label.setGeometry(235, crud_y + 125, 150, 25)
        self.security_answer_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        self.security_answer_field = QLineEdit(self.shape3_content)
        self.security_answer_field.setStyleSheet("""
                                    QLineEdit {
                                    background-color: rgb(50, 50, 50);
                                    border: 1px solid rgba(150, 150, 150, 0);
                                    border-radius: 0px;
                                    padding: 5px 12px;
                                    color: rgb(225, 225, 225);
                                    font-family: Poppins;
                                    font-size: 14px;
                                    }""")
        self.security_answer_field.setGeometry(235, crud_y + 150, 200, 30)

        # Password and Confirm Password (row 4, 200x30 each)
        self.password_label = QLabel("Password:", self.shape3_content)
        self.password_label.setGeometry(20, crud_y + 185, 100, 25)
        self.password_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        self.password_field = QLineEdit(self.shape3_content)
        self.password_field.setStyleSheet("""
                                    QLineEdit {
                                    background-color: rgb(50, 50, 50);
                                    border: 1px solid rgba(150, 150, 150, 0);
                                    border-radius: 0px;
                                    padding: 5px 12px;
                                    color: rgb(225, 225, 225);
                                    font-family: Poppins;
                                    font-size: 14px;
                                    }""")
        self.password_field.setGeometry(20, crud_y + 210, 200, 30)

        self.confirm_password_label = QLabel("Confirm Password:", self.shape3_content)
        self.confirm_password_label.setGeometry(235, crud_y + 185, 150, 25)
        self.confirm_password_label.setStyleSheet("color: rgb(200, 200, 200); font-family: Poppins; font-size: 12px; background-color: transparent; border: none;")

        self.confirm_password_field = QLineEdit(self.shape3_content)
        self.confirm_password_field.setStyleSheet("""
                                    QLineEdit {
                                    background-color: rgb(50, 50, 50);
                                    border: 1px solid rgba(150, 150, 150, 0);
                                    border-radius: 0px;
                                    padding: 5px 12px;
                                    color: rgb(225, 225, 225);
                                    font-family: Poppins;
                                    font-size: 14px;
                                    }""")
        self.confirm_password_field.setGeometry(235, crud_y + 210, 200, 30)

        # Buttons (below all fields)
        self.create_btn = QPushButton("Create", self.shape3_content)
        self.create_btn.setGeometry(20, crud_y + 250, 100, 30)
        self.create_btn.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(0, 150, 0);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 0);
                                        padding: 5px 12px;
                                        font-family: Poppins;
                                        font-size: 14px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(0, 180, 0);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(0, 120, 0);
                                        }""")
        self.create_btn.clicked.connect(self.handle_create_account)

        self.update_btn = QPushButton("Update", self.shape3_content)
        self.update_btn.setGeometry(130, crud_y + 250, 100, 30)
        self.update_btn.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(150, 150, 0);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 0);
                                        padding: 5px 12px;
                                        font-family: Poppins;
                                        font-size: 14px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(180, 180, 0);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(120, 120, 0);
                                        }""")
        self.update_btn.clicked.connect(self.handle_update_account)

        self.clear_btn = QPushButton("Clear", self.shape3_content)
        self.clear_btn.setGeometry(240, crud_y + 250, 100, 30)
        self.clear_btn.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(100, 100, 100);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 0);
                                        padding: 5px 12px;
                                        font-family: Poppins;
                                        font-size: 14px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(120, 120, 120);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(80, 80, 80);
                                        }""")
        self.clear_btn.clicked.connect(self.clear_account_fields)

        # Store all accounts
        self.all_accounts = []

    def switch_view(self, view):
        """Switch between REPORTS and ACCOUNTS views"""
        self.current_view = view
        
        # Update button styles
        if view == "reports":
            self.reports_btn.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(120, 0, 0);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 0);
                                        padding: 8px 12px;
                                        font-family: Poppins;
                                        font-size: 16px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(150, 0, 0);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(100, 0, 0);
                                        }""")
            self.accounts_btn.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(60, 60, 60);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 0);
                                        padding: 8px 12px;
                                        font-family: Poppins;
                                        font-size: 16px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(80, 80, 80);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(50, 50, 50);
                                        }""")
            # Show reports components
            self.registered_card.show()
            self.pending_card.show()
            self.approved_card.show()
            self.rejected_card.show()
            self.reports_filter_label.show()
            self.reports_search.show()
            self.date_from_label.show()
            self.reports_date_from.show()
            self.date_to_label.show()
            self.reports_date_to.show()
            self.reports_status.show()
            self.reports_table.show()
            self.stats_registered_label.show()
            self.stats_pending_label.show()
            self.stats_approved_label.show()
            self.stats_rejected_label.show()
            self.graph_canvas.show()
            self.shape3_scroll.hide()
            # Hide accounts components
            self.accounts_filter_label.hide()
            self.accounts_search.hide()
            self.accounts_role.hide()
            self.accounts_table.hide()
            self.account_name_label.hide()
            self.account_name_field.hide()
            self.username_label.hide()
            self.username_field.hide()
            self.password_label.hide()
            self.password_field.hide()
            self.confirm_password_label.hide()
            self.confirm_password_field.hide()
            self.role_label.hide()
            self.role_field.hide()
            self.security_question_label.hide()
            self.security_question_field.hide()
            self.security_answer_label.hide()
            self.security_answer_field.hide()
            self.create_btn.hide()
            self.update_btn.hide()
            self.clear_btn.hide()
            # Load reports data
            self.load_reports_data()
        else:  # accounts
            self.reports_btn.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(60, 60, 60);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 0);
                                        padding: 8px 12px;
                                        font-family: Poppins;
                                        font-size: 16px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(80, 80, 80);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(50, 50, 50);
                                        }""")
            self.accounts_btn.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(120, 0, 0);
                                        color: rgb(200, 200, 200);
                                        border-radius: 0px;
                                        border: 1px solid rgba(150, 150, 150, 0);
                                        padding: 8px 12px;
                                        font-family: Poppins;
                                        font-size: 16px;
                                        font-weight: bold;
                                        }
                                    QPushButton:hover {
                                        background-color: rgb(150, 0, 0);
                                        }
                                    QPushButton:pressed {
                                        background-color: rgb(100, 0, 0);
                                        }""")
            # Hide reports components
            self.registered_card.hide()
            self.pending_card.hide()
            self.approved_card.hide()
            self.rejected_card.hide()
            self.reports_filter_label.hide()
            self.reports_search.hide()
            self.date_from_label.hide()
            self.reports_date_from.hide()
            self.date_to_label.hide()
            self.reports_date_to.hide()
            self.reports_status.hide()
            self.reports_table.hide()
            self.stats_registered_label.hide()
            self.stats_pending_label.hide()
            self.stats_approved_label.hide()
            self.stats_rejected_label.hide()
            self.graph_canvas.hide()
            self.shape3_scroll.show()
            # Show accounts components
            self.accounts_filter_label.show()
            self.accounts_search.show()
            self.accounts_role.show()
            self.accounts_table.show()
            self.account_name_label.show()
            self.account_name_field.show()
            self.username_label.show()
            self.username_field.show()
            self.password_label.show()
            self.password_field.show()
            self.confirm_password_label.show()
            self.confirm_password_field.show()
            self.role_label.show()
            self.role_field.show()
            self.security_question_label.show()
            self.security_question_field.show()
            self.security_answer_label.show()
            self.security_answer_field.show()
            self.create_btn.show()
            self.update_btn.show()
            self.clear_btn.show()
            # Load accounts data
            self.load_accounts_data()

    def load_reports_data(self):
        """Load registration records and statistics"""
        self.all_registration_records = self.controller.get_all_registrations()
        
        # Calculate statistics
        total = len(self.all_registration_records)
        pending = sum(1 for r in self.all_registration_records if r.get("Status") == "Pending")
        approved = sum(1 for r in self.all_registration_records if r.get("Status") == "Approved")
        rejected = sum(1 for r in self.all_registration_records if r.get("Status") == "Rejected")
        
        # Update cards
        self.registered_value.setText(str(total))
        self.pending_value.setText(str(pending))
        self.approved_value.setText(str(approved))
        self.rejected_value.setText(str(rejected))
        
        # Update labels below table
        self.stats_registered_label.setText(f"Registered: {total}")
        self.stats_pending_label.setText(f"Pending: {pending}")
        self.stats_approved_label.setText(f"Approved: {approved}")
        self.stats_rejected_label.setText(f"Rejected: {rejected}")
        
        # Apply filters to populate table
        self.apply_reports_filters()
        
        # Update graph
        self.update_graph()

    def apply_reports_filters(self):
        """Apply filters to reports table"""
        search_text = self.reports_search.text().lower()
        date_from = self.reports_date_from.date().toPyDate()
        date_to = self.reports_date_to.date().toPyDate()
        status_filter = self.reports_status.currentText()
        
        filtered_records = []
        for record in self.all_registration_records:
            # Search filter
            if search_text:
                searchable = f"{record.get('RegistrationID', '')} {record.get('StudentID', '')}".lower()
                if search_text not in searchable:
                    continue
            
            # Date range filter
            reg_date = record.get("SubmittedAt")
            if reg_date:
                if isinstance(reg_date, str):
                    from datetime import datetime
                    try:
                        reg_date = datetime.strptime(reg_date, "%Y-%m-%d %H:%M:%S").date()
                    except:
                        try:
                            reg_date = datetime.strptime(reg_date, "%Y-%m-%d").date()
                        except:
                            reg_date = None
                else:
                    reg_date = reg_date.date() if hasattr(reg_date, 'date') else None
                
                if reg_date:
                    if reg_date < date_from or reg_date > date_to:
                        continue
            
            # Status filter
            if status_filter != "ALL" and record.get("Status") != status_filter:
                continue
            
            filtered_records.append(record)
        
        # Populate table
        self.reports_table.setRowCount(len(filtered_records))
        for row, record in enumerate(filtered_records):
            self.reports_table.setItem(row, 0, QTableWidgetItem(str(record.get("RegistrationID", "N/A"))))
            self.reports_table.setItem(row, 1, QTableWidgetItem(str(record.get("StudentID", "N/A"))))
            # Show EmployeeID (ValidatorID) instead of name
            validator_id = record.get("ValidatorID") or record.get("ValidatedBy") or "N/A"
            self.reports_table.setItem(row, 2, QTableWidgetItem(str(validator_id)))
            reg_date = record.get("SubmittedAt")
            if reg_date:
                if isinstance(reg_date, str):
                    date_str = reg_date
                else:
                    date_str = reg_date.strftime("%Y-%m-%d")
            else:
                date_str = "N/A"
            self.reports_table.setItem(row, 3, QTableWidgetItem(date_str))
            status_item = QTableWidgetItem(record.get("Status", "N/A"))
            status = record.get("Status", "")
            if status == "Approved":
                status_item.setForeground(QColor(0, 255, 0))
            elif status == "Rejected":
                status_item.setForeground(QColor(255, 0, 0))
            elif status == "Pending":
                status_item.setForeground(QColor(255, 255, 0))
            self.reports_table.setItem(row, 4, status_item)
        
        # Resize columns
        header = self.reports_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

    def update_graph(self):
        """Update the monthly registrations graph"""
        monthly_data = self.controller.get_monthly_registrations()
        
        # Prepare data
        months = []
        counts = []
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Create a dictionary for all months
        month_dict = {i+1: 0 for i in range(12)}
        for data in monthly_data:
            month_dict[data['month']] = data['count']
        
        # Convert to lists
        for month_num in range(1, 13):
            months.append(month_names[month_num - 1])
            counts.append(month_dict[month_num])
        
        # Clear previous plot
        self.graph_figure.clear()
        ax = self.graph_figure.add_subplot(111)
        
        # Create line graph
        ax.plot(months, counts, marker='o', linewidth=1.5, markersize=4, color='#c80000')
        ax.set_xlabel('Month', fontsize=8, color='white')
        ax.set_ylabel('Registrations', fontsize=8, color='white')
        ax.set_title('Monthly Registrations', fontsize=10, color='white', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#3c3c3c')
        self.graph_figure.patch.set_facecolor('#3c3c3c')
        ax.tick_params(colors='white', labelsize=7)
        
        # Rotate x-axis labels more and adjust layout
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=90, ha='center', fontsize=7)
        self.graph_figure.tight_layout(pad=1.0)
        
        self.graph_canvas.draw()

    def load_accounts_data(self):
        """Load all accounts"""
        self.all_accounts = self.controller.get_all_accounts()
        self.apply_accounts_filters()

    def apply_accounts_filters(self):
        """Apply filters to accounts table"""
        search_text = self.accounts_search.text().lower()
        role_filter = self.accounts_role.currentText()
        
        filtered_accounts = []
        for account in self.all_accounts:
            # Search filter
            if search_text:
                searchable = f"{account.get('AccountID', '')} {account.get('Username', '')}".lower()
                if search_text not in searchable:
                    continue
            
            # Role filter
            if role_filter != "ALL" and account.get("Role", "").lower() != role_filter.lower():
                continue
            
            filtered_accounts.append(account)
        
        # Populate table
        self.accounts_table.setRowCount(len(filtered_accounts))
        for row, account in enumerate(filtered_accounts):
            self.accounts_table.setItem(row, 0, QTableWidgetItem(str(account.get("AccountID", "N/A"))))
            self.accounts_table.setItem(row, 1, QTableWidgetItem(str(account.get("Username", "N/A"))))
            # UUID (StudentID or EmployeeID)
            uuid_value = account.get("UUID") or "N/A"
            self.accounts_table.setItem(row, 2, QTableWidgetItem(str(uuid_value)))
            # Mask password
            password = account.get("Password", "")
            masked_password = "*" * len(password) if password else "N/A"
            self.accounts_table.setItem(row, 3, QTableWidgetItem(masked_password))
            self.accounts_table.setItem(row, 4, QTableWidgetItem(str(account.get("SecurityQuestion", "N/A"))))
            # Mask security answer
            sec_answer = account.get("SecurityAnswer", "")
            masked_answer = "*" * len(sec_answer) if sec_answer else "N/A"
            self.accounts_table.setItem(row, 5, QTableWidgetItem(masked_answer))
        
        # Resize columns
        header = self.accounts_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

    def on_account_selected(self):
        """Handle account selection from table"""
        current_row = self.accounts_table.currentRow()
        if current_row >= 0:
            account_id_item = self.accounts_table.item(current_row, 0)
            if account_id_item:
                account_id = account_id_item.text()
                account = self.controller.get_account_by_id(account_id)
                if account:
                    self.selected_account_id = account_id
                    username = account.get("Username", "")
                    self.account_name_field.setText(username)
                    self.account_name_field.setReadOnly(True)  # Read-only when viewing existing account
                    self.username_field.setText(username)
                    self.username_field.setReadOnly(True)  # Read-only when viewing existing account
                    self.password_field.setText(account.get("Password", ""))
                    self.confirm_password_field.clear()
                    
                    # Check if student - disable role if student
                    if account.get("Role", "").lower() == "student":
                        self.role_field.setEnabled(False)
                        self.role_field.clear()
                        self.role_field.addItems(["student"])
                        self.role_field.setCurrentText("student")
                    else:
                        self.role_field.setEnabled(True)
                        self.role_field.clear()
                        self.role_field.addItems(["admin", "registrar"])
                        self.role_field.setCurrentText(account.get("Role", ""))
                    
                    # Set security question in combo box
                    security_question = account.get("SecurityQuestion", "")
                    if security_question:
                        index = self.security_question_field.findText(security_question)
                        if index >= 0:
                            self.security_question_field.setCurrentIndex(index)
                        else:
                            # If question not in list, add it and select it
                            self.security_question_field.addItem(security_question)
                            self.security_question_field.setCurrentText(security_question)
                    self.security_answer_field.setText(account.get("SecurityAnswer", ""))

    def handle_create_account(self):
        """Handle create account button"""
        username = self.username_field.text().strip()
        password = self.password_field.text().strip()
        confirm_password = self.confirm_password_field.text().strip()
        role = self.role_field.currentText()
        security_question = self.security_question_field.currentText()
        security_answer = self.security_answer_field.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Username and Password are required.")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
            return
        
        account_id = self.controller.create_account(username, password, role, security_question, security_answer)
        if account_id:
            QMessageBox.information(self, "Success", "Account created successfully.")
            self.clear_account_fields()
            self.load_accounts_data()
        else:
            QMessageBox.warning(self, "Error", "Failed to create account. Username may already exist.")

    def handle_update_account(self):
        """Handle update account button"""
        if not self.selected_account_id:
            QMessageBox.warning(self, "No Selection", "Please select an account to update.")
            return
        
        password = self.password_field.text().strip()
        confirm_password = self.confirm_password_field.text().strip()
        role = self.role_field.currentText()
        security_question = self.security_question_field.currentText()
        security_answer = self.security_answer_field.text().strip()
        
        # Validate password confirmation if password is provided
        if password and password != confirm_password:
            QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
            return
        
        # Check if student - role cannot be changed
        if self.controller.is_student_account(self.selected_account_id):
            role = None  # Don't update role for students
        
        success = self.controller.update_account(
            self.selected_account_id,
            password=password if password else None,
            role=role if role else None,
            security_question=security_question if security_question else None,
            security_answer=security_answer if security_answer else None
        )
        
        if success:
            QMessageBox.information(self, "Success", "Account updated successfully.")
            self.load_accounts_data()
        else:
            QMessageBox.warning(self, "Error", "Failed to update account.")

    def clear_account_fields(self):
        """Clear account fields"""
        self.selected_account_id = None
        self.account_name_field.clear()
        self.account_name_field.setReadOnly(True)  # Always read-only
        self.username_field.clear()
        self.username_field.setReadOnly(False)  # Editable when creating new account
        self.password_field.clear()
        self.confirm_password_field.clear()
        self.role_field.setCurrentIndex(0)
        self.security_question_field.setCurrentIndex(0)
        self.security_answer_field.clear()
        self.role_field.setEnabled(True)
        self.role_field.clear()
        self.role_field.addItems(["admin", "registrar"])

    def handle_logout(self):
        """Handle logout button click"""
        self.main_window.current_user = None
        self.main_window.switch_view("login")
