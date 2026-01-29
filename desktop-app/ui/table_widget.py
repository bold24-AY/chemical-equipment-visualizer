"""
Table widget for displaying equipment data.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QGroupBox, QHeaderView)
from PyQt5.QtCore import Qt


class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Group box
        group = QGroupBox("Equipment Data")
        group_layout = QVBoxLayout()
        
        # Create table
        self.table = QTableWidget()
        self.table.setMinimumHeight(200)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        
        # Table styling
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #e0e6ed;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:alternate {
                background-color: #f5f7fa;
            }
            QHeaderView::section {
                background-color: #1a5490;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Adjust column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        group_layout.addWidget(self.table)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        self.setLayout(layout)
    
    def update_data(self, raw_data):
        """
        Update table with equipment data.
        """
        if not raw_data:
            self.table.setRowCount(0)
            return
        
        self.table.setRowCount(len(raw_data))
        
        for row_idx, row_data in enumerate(raw_data):
            # Equipment Name
            item = QTableWidgetItem(row_data.get('Equipment Name', ''))
            self.table.setItem(row_idx, 0, item)
            
            # Type
            item = QTableWidgetItem(row_data.get('Type', ''))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 1, item)
            
            # Flowrate
            flowrate = row_data.get('Flowrate', 0)
            item = QTableWidgetItem(f"{flowrate:.2f}")
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 2, item)
            
            # Pressure
            pressure = row_data.get('Pressure', 0)
            item = QTableWidgetItem(f"{pressure:.2f}")
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 3, item)
            
            # Temperature
            temperature = row_data.get('Temperature', 0)
            item = QTableWidgetItem(f"{temperature:.2f}")
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 4, item)
    
    def clear(self):
        """
        Clear table data.
        """
        self.table.setRowCount(0)
