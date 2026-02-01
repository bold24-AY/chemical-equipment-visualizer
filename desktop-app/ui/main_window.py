"""
Main window for the desktop application.
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QPushButton, QLabel, QMessageBox,
                             QDialog, QLineEdit, QFormLayout, QDialogButtonBox,
                             QFileDialog, QStatusBar, QTableWidget, QTableWidgetItem,
                             QHeaderView, QScrollArea, QSizePolicy, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QIcon

from .upload_widget import UploadWidget
from .summary_widget import SummaryWidget
from .chart_widget import ChartWidget
from .table_widget import TableWidget


from PyQt5.QtSvg import QSvgWidget

class LoginDialog(QDialog):
    """Login dialog for authentication."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login - Chemical Equipment Visualizer")
        self.setModal(True)
        self.setFixedSize(400, 320) # Increased height for logo
        
        layout = QFormLayout()

        # Logo
        logo = QSvgWidget("assets/logo.svg")
        logo.setFixedSize(80, 80)
        # Center logo
        logo_container = QHBoxLayout()
        logo_container.addStretch()
        logo_container.addWidget(logo)
        logo_container.addStretch()
        layout.addRow(logo_container)
        
        # Title
        title = QLabel("Chemical Equipment Visualizer")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a5490; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        layout.addRow(title)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")
        layout.addRow(self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")
        layout.addRow(self.password_input)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        # Demo credentials hint
        hint = QLabel("Demo: trial12 / Trial@1234")
        hint.setStyleSheet("color: #666; font-size: 11px; margin-top: 10px;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addRow(hint)

        # Sign up link
        signup_label = QLabel('Not a user? <a href="#">Sign up</a>')
        signup_label.setStyleSheet("color: #666; font-size: 11px; margin-top: 5px;")
        signup_label.setAlignment(Qt.AlignCenter)
        signup_label.setOpenExternalLinks(False) # Or True if valid URL
        signup_label.linkActivated.connect(self.switch_to_signup)
        layout.addRow(signup_label)
        
        self.setLayout(layout)
    
    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()

    def switch_to_signup(self):
        """Close login and inform caller to show signup."""
        self.done(10) # Custom return code for "Switch to Signup"


class SignupDialog(QDialog):
    """Signup dialog for registration."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign Up - Chemical Equipment Visualizer")
        self.setModal(True)
        self.setFixedSize(400, 380) # Increased height for logo
        
        layout = QFormLayout()

        # Logo
        logo = QSvgWidget("assets/logo.svg")
        logo.setFixedSize(60, 60)
        # Center logo
        logo_container = QHBoxLayout()
        logo_container.addStretch()
        logo_container.addWidget(logo)
        logo_container.addStretch()
        layout.addRow(logo_container)
        
        # Title
        title = QLabel("Create Account")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a5490; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addRow(title)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose username")
        self.username_input.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px;")
        layout.addRow("Username:", self.username_input)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email (Optional)")
        self.email_input.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px;")
        layout.addRow("Email:", self.email_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px;")
        layout.addRow("Password:", self.password_input)

        # Confirm Password
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setPlaceholderText("Confirm password")
        self.confirm_input.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px;")
        layout.addRow("Confirm:", self.confirm_input)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        # Login link
        login_label = QLabel('Already a user? <a href="#">Sign in</a>')
        login_label.setStyleSheet("color: #666; font-size: 11px; margin-top: 10px;")
        login_label.setAlignment(Qt.AlignCenter)
        login_label.setOpenExternalLinks(False)
        login_label.linkActivated.connect(self.switch_to_login) 
        layout.addRow(login_label)
        
        self.setLayout(layout)
    
    def get_credentials(self):
        return self.username_input.text(), self.password_input.text(), self.email_input.text()
        
    def switch_to_login(self):
        """Close signup and inform caller to show login."""
        self.done(10) # Custom return code for "Switch to Login"


class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.current_dataset = None
        self.animations_enabled = True
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e0e6ed;
                background: white;
                border-top: 2px solid #e0e6ed; /* Consistent border */
            }
            QTabBar::tab {
                background: transparent;
                color: #666;
                padding: 12px 24px;
                margin: 0;
                border-bottom: 3px solid transparent;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                color: #1a5490;
                font-weight: bold;
                border-bottom: 3px solid #1a5490;
                background-color: white;
            }
            QTabBar::tab:hover {
                background-color: #f8fafc;
            }
        """)
        
        # Upload tab
        self.upload_widget = UploadWidget(self.api_client)
        self.upload_widget.upload_success.connect(self.on_upload_success)
        self.tabs.addTab(self.upload_widget, "📤 Upload")
        
        # Dashboard tab
        self.dashboard_widget = self.create_dashboard()
        self.tabs.addTab(self.dashboard_widget, "📊 Dashboard")
        
        # History tab
        self.history_widget = self.create_history_tab()
        self.tabs.addTab(self.history_widget, "📜 History")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
        central_widget.setLayout(main_layout)
        
        # Apply global stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #f5f7fa, stop:1 #eef1f5);
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e6ed;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #0f3d6e, stop:1 #1a5490);
                color: rgba(255, 255, 255, 0.8);
                padding: 5px;
            }
        """)
    
    def create_header(self):
        """Create application header."""
        header = QWidget()
        header.setObjectName("header")
        # Using border-image to cover the widget
        # Assuming run from desktop-app directory or assets in CWD/assets
        header.setStyleSheet("""
            QWidget#header {
                border-image: url(assets/chemical_lab_header.jpeg) 0 0 0 0 stretch stretch;
            }
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Overlay widget for darkening
        overlay = QWidget()
        overlay.setStyleSheet("""
            QWidget {
                background-color: rgba(26, 84, 144, 0.85); 
            }
            QLabel {
                background-color: transparent;
            }
        """)
        header_layout.addWidget(overlay)
        
        layout = QHBoxLayout(overlay)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Logo + Title
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        
        logo_label = QLabel()
        logo_label.setPixmap(QIcon("assets/logo.svg").pixmap(QSize(32, 32)))
        title_layout.addWidget(logo_label)
        
        title = QLabel("Chemical Equipment Visualizer")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        title_layout.addWidget(title)
        
        title_layout.addStretch()
        layout.addLayout(title_layout)
        

        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1a5490;
                border: none;
            }
            QPushButton:hover {
                background-color: #e8eef5;
            }
        """)
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)
        
        # Download report button
        report_btn = QPushButton("📄 Download Report")
        report_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1a5490;
                border: none;
            }
            QPushButton:hover {
                background-color: #e8eef5;
            }
        """)
        report_btn.clicked.connect(self.download_report)
        layout.addWidget(report_btn)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        return header
    
    def create_dashboard(self):
        """Create dashboard tab with all visualization widgets."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.dashboard_content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Dataset Context Label (Point 10)
        self.context_label = QLabel("Waiting for data...")
        self.context_label.setStyleSheet("font-size: 14px; color: #666; font-style: italic;")
        self.context_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.context_label)
        
        # Summary cards
        self.summary_widget = SummaryWidget()
        self.summary_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(self.summary_widget)
        
        # Charts
        self.chart_widget = ChartWidget()
        self.chart_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.chart_widget.setMinimumHeight(450) # Increased height for 2x2 grid
        layout.addWidget(self.chart_widget)
        
        # Data table
        self.table_widget = TableWidget()
        self.table_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.table_widget.setMinimumHeight(250)
        layout.addWidget(self.table_widget)
        
        self.dashboard_content.setLayout(layout)
        scroll_area.setWidget(self.dashboard_content)
        
        # Opacity effect for transition
        self.opacity_effect = QGraphicsOpacityEffect(self.dashboard_content)
        self.dashboard_content.setGraphicsEffect(self.opacity_effect)
        
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(300)
        self.fade_anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        return scroll_area

    def create_history_tab(self):
        """Create history tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(['Filename', 'Uploaded At', 'Items'])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.history_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.history_table)
        widget.setLayout(layout)
        return widget
    

    
    def load_data(self):
        """Load latest dataset from backend."""
        if self.current_dataset and self.animations_enabled:
            # Fade out
            self.fade_anim.setStartValue(1.0)
            self.fade_anim.setEndValue(0.5)
            self.fade_anim.start()
            
            # Delay data update slightly
            QTimer.singleShot(300, self._perform_data_load)
        else:
            self._perform_data_load()
            
    def _perform_data_load(self):
        try:
            self.statusBar.showMessage("Loading data...")
            
            # Get latest summary
            data = self.api_client.get_summary()
            self.current_dataset = data
            
            # Update widgets
            self.context_label.setText(f"Showing analysis for: {data['file_name']}")
            self.summary_widget.update_summary(data['summary'])
            self.chart_widget.update_charts(data['summary'], data['raw_data'])
            self.table_widget.update_data(data['raw_data'])
            
            # Get history
            history_data = self.api_client.get_history()
            self.update_history(history_data)

            self.statusBar.showMessage(f"Loaded: {data['file_name']}")
            
            if self.animations_enabled:
                # Fade in
                self.fade_anim.setStartValue(0.5)
                self.fade_anim.setEndValue(1.0)
                self.fade_anim.start()
            else:
                self.opacity_effect.setOpacity(1.0)
            
        except Exception as e:
            self.statusBar.showMessage("No data available")
            self.opacity_effect.setOpacity(1.0)

    def update_history(self, history_data):
        """Update history table."""
        from datetime import datetime
        self.history_table.setRowCount(len(history_data))
        for i, item in enumerate(history_data):
            # Filename
            self.history_table.setItem(i, 0, QTableWidgetItem(item['file_name']))
            
            # Date
            try:
                dt = datetime.fromisoformat(item['uploaded_at'].replace('Z', '+00:00'))
                date_str = dt.strftime('%b %d, %Y %H:%M') # "Jan 28, 2024 14:30"
            except:
                date_str = item['uploaded_at']
            self.history_table.setItem(i, 1, QTableWidgetItem(date_str))
            
            # Items
            count = item['summary']['total_equipment']
            self.history_table.setItem(i, 2, QTableWidgetItem(str(count)))
    
    def on_upload_success(self):
        """Handle successful upload."""
        self.load_data()
        self.tabs.setCurrentIndex(1)  # Switch to dashboard
    
    def download_report(self):
        """Download PDF report."""
        if not self.current_dataset:
            QMessageBox.warning(
                self,
                "No Data",
                "Please upload a dataset first."
            )
            return
        
        try:
            # Ask user where to save
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Report",
                f"equipment_report_{self.current_dataset['id']}.pdf",
                "PDF Files (*.pdf)"
            )
            
            if file_path:
                self.statusBar.showMessage("Generating report...")
                self.api_client.download_report(
                    self.current_dataset['id'],
                    file_path
                )
                self.statusBar.showMessage(f"Report saved: {file_path}")
                QMessageBox.information(
                    self,
                    "Success",
                    f"Report downloaded successfully!\n{file_path}"
                )
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Download Error",
                f"Failed to download report:\n{str(e)}"
            )
            self.statusBar.showMessage("Report download failed")
    
    def logout(self):
        """Logout and close application."""
        try:
            self.api_client.logout()
        except:
            pass
        self.close()
    
    def closeEvent(self, event):
        """Handle window close event."""
        reply = QMessageBox.question(
            self,
            'Confirm Exit',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
