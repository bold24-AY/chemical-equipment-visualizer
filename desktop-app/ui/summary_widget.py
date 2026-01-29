"""
Summary widget for displaying dataset statistics.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGroupBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CardWidget(QFrame):
    """
    Custom card widget matching the web frontend design.
    """
    def __init__(self, title, icon, color, bg_color):
        super().__init__()
        self.setObjectName("card")
        self.setStyleSheet(f"""
            QFrame#card {{
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                border-left: 5px solid {color};
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Icon container
        icon_container = QLabel(icon)
        icon_container.setAlignment(Qt.AlignCenter)
        icon_container.setFixedSize(50, 50)
        icon_container.setFont(QFont("Segoe UI Emoji", 24))
        icon_container.setStyleSheet(f"""
            background-color: {bg_color};
            color: {color};
            border-radius: 25px;
        """)
        layout.addWidget(icon_container)
        
        # Text container
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #6B7280; font-size: 14px; font-weight: 500;")
        
        self.value_label = QLabel("0")
        self.value_label.setStyleSheet("color: #111827; font-size: 28px; font-weight: bold;")
        
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.value_label)
        layout.addLayout(text_layout)
        
        layout.addStretch()
        self.setLayout(layout)

    def set_value(self, value):
        self.value_label.setText(str(value))


class SummaryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Group box (optional, can remove if we want pure dashboard look, but keeping for now)
        # Replacing GroupBox with just a label title or direct layout to match "Dashboard" header look from web
        # but user has "Summary Statistics" header in their screenshot.
        
        title_label = QLabel("Summary Statistics")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #111827; margin-bottom: 10px;")
        layout.addWidget(title_label)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        # Create stat cards with web-styled colors and icons
        # Total: Navy Blue
        self.total_card = CardWidget("Total Equipment", "📊", "#1a5490", "rgba(26, 84, 144, 0.1)")
        
        # Flowrate: Green
        self.flowrate_card = CardWidget("Avg Flowrate", "💧", "#2ecc71", "rgba(46, 204, 113, 0.1)")
        
        # Pressure: Blue/Purple
        self.pressure_card = CardWidget("Avg Pressure", "⚙️", "#3B82F6", "rgba(59, 130, 246, 0.1)")
        
        # Temperature: Red
        self.temperature_card = CardWidget("Avg Temperature", "🌡️", "#EF4444", "rgba(239, 68, 68, 0.1)")
        
        cards_layout.addWidget(self.total_card)
        cards_layout.addWidget(self.flowrate_card)
        cards_layout.addWidget(self.pressure_card)
        cards_layout.addWidget(self.temperature_card)
        
        layout.addLayout(cards_layout)
        self.setLayout(layout)
    
    def update_summary(self, summary):
        """
        Update summary statistics from dataset.
        """
        if not summary:
            self.clear()
            return
        
        # Update values
        self.total_card.set_value(summary['total_equipment'])
        self.flowrate_card.set_value(f"{summary['average_flowrate']:.2f}")
        self.pressure_card.set_value(f"{summary['average_pressure']:.2f}")
        self.temperature_card.set_value(f"{summary['average_temperature']:.2f}")
    
    def clear(self):
        """
        Clear all summary values.
        """
        self.total_card.set_value("0")
        self.flowrate_card.set_value("0.00")
        self.pressure_card.set_value("0.00")
        self.temperature_card.set_value("0.00")
