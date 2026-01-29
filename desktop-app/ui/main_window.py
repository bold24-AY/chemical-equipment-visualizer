"""
Main window for the desktop application.
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QPushButton, QLabel, QMessageBox,
                             QDialog, QLineEdit, QFormLayout, QDialogButtonBox,
                             QFileDialog, QStatusBar, QTableWidget, QTableWidgetItem,
                             QHeaderView, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from .upload_widget import UploadWidget
from .summary_widget import SummaryWidget
from .chart_widget import ChartWidget
from .table_widget import TableWidget


class LoginDialog(QDialog):
    """Login dialog for authentication."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login - Chemical Equipment Visualizer")
        self.setModal(True)
        self.setFixedSize(400, 200)
        
        layout = QFormLayout()
        
        # Title
        title = QLabel("Chemical Equipment Visualizer")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a5490; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addRow(title)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        layout.addRow("Username:", self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        layout.addRow("Password:", self.password_input)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        # Demo credentials hint
        hint = QLabel("Demo: admin / admin")
        hint.setStyleSheet("color: #666; font-size: 11px; margin-top: 10px;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addRow(hint)
        
        self.setLayout(layout)
    
    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()


class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.current_dataset = None
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
            }
            QTabBar::tab {
                background: #f5f7fa;
                color: #666;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #1a5490;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #e8eef5;
            }
        """)
        
        # Upload tab
        self.upload_widget = UploadWidget(self.api_client)
        self.upload_widget.upload_success.connect(self.on_upload_success)
        self.tabs.addTab(self.upload_widget, "📤 Upload")
        
        # Dashboard tab
        dashboard_widget = self.create_dashboard()
        self.tabs.addTab(dashboard_widget, "📊 Dashboard")
        
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
                background-color: #f5f7fa;
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
        """)
    
    def create_header(self):
        """Create application header."""
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #1a5490, stop:1 #2e7fc9);
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Title
        title = QLabel("🧪 Chemical Equipment Visualizer")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1a5490;
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
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        header.setLayout(layout)
        return header
    
    def create_dashboard(self):
        """Create dashboard tab with all visualization widgets."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        dashboard_content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Summary cards
        self.summary_widget = SummaryWidget()
        self.summary_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(self.summary_widget)
        
        # Charts
        self.chart_widget = ChartWidget()
        self.chart_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.chart_widget.setMinimumHeight(350) 
        layout.addWidget(self.chart_widget)
        
        # Data table
        self.table_widget = TableWidget()
        self.table_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.table_widget.setMinimumHeight(250)
        layout.addWidget(self.table_widget)
        
        dashboard_content.setLayout(layout)
        scroll_area.setWidget(dashboard_content)
        
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
        try:
            self.statusBar.showMessage("Loading data...")
            
            # Get latest summary
            data = self.api_client.get_summary()
            self.current_dataset = data
            
            # Update widgets
            self.summary_widget.update_summary(data['summary'])
            self.chart_widget.update_charts(data['summary'], data['raw_data'])
            self.table_widget.update_data(data['raw_data'])
            
            # Get history
            history_data = self.api_client.get_history()
            self.update_history(history_data)

            self.statusBar.showMessage(f"Loaded: {data['file_name']}")
            
        except Exception as e:
            self.statusBar.showMessage("No data available")
            # Don't show popup on auto-refresh or init, but here we do
            # actually we don't have auto-refresh yet
            pass

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
