"""
Upload widget for CSV file selection and upload.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QMessageBox, QGroupBox)
from PyQt5.QtCore import pyqtSignal, Qt


class UploadWidget(QWidget):
    upload_success = pyqtSignal()
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.selected_file = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Group box
        group = QGroupBox("Upload Equipment Data")
        group_layout = QVBoxLayout()
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("padding: 10px; background: #f0f0f0; border-radius: 5px;")
        file_layout.addWidget(self.file_label)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        browse_btn.setFixedWidth(100)
        file_layout.addWidget(browse_btn)
        
        group_layout.addLayout(file_layout)
        
        # Upload button
        self.upload_btn = QPushButton("Upload & Analyze")
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a5490;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14406f;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        group_layout.addWidget(self.upload_btn)
        
        # Info section (Contextual Help)
        self.info_btn = QPushButton("Show Required Columns ⓘ")
        self.info_btn.setCheckable(True)
        self.info_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #1a5490;
                text-align: left;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #f0f7ff;
            }
        """)
        self.info_btn.clicked.connect(self.toggle_info)
        group_layout.addWidget(self.info_btn)
        
        self.info_label = QLabel(
            "• Equipment Name\n"
            "• Type\n"
            "• Flowrate (numeric)\n"
            "• Pressure (numeric)\n"
            "• Temperature (numeric)"
        )
        self.info_label.setStyleSheet("padding: 10px; background: #e8eef5; border-radius: 5px; margin-left: 10px;")
        self.info_label.setVisible(False)
        group_layout.addWidget(self.info_label)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path.split('/')[-1])
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        if not self.selected_file:
            return
        
        try:
            self.upload_btn.setEnabled(False)
            self.upload_btn.setText("Uploading...")
            
            # Upload to backend
            result = self.api_client.upload_csv(self.selected_file)
            
            QMessageBox.information(
                self,
                "Success",
                "File uploaded and analyzed successfully!"
            )
            
            # Reset
            self.selected_file = None
            self.file_label.setText("No file selected")
            self.upload_btn.setText("Upload & Analyze")
            
            # Emit success signal
            self.upload_success.emit()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Upload Error",
                f"Failed to upload file:\n{str(e)}"
            )
            self.upload_btn.setEnabled(True)
            self.upload_btn.setText("Upload & Analyze")
    
    def toggle_info(self):
        """Toggle visibility of requirements info."""
        if self.info_btn.isChecked():
            self.info_label.setVisible(True)
            self.info_btn.setText("Hide Required Columns ⓘ")
        else:
            self.info_label.setVisible(False)
            self.info_btn.setText("Show Required Columns ⓘ")
