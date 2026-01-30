"""
Summary widget for displaying dataset statistics.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGroupBox, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class CardWidget(QFrame):
    """
    Custom card widget matching the web frontend design.
    """
    def __init__(self, title, icon, color, bg_color, unit=""):
        super().__init__()
        self.setObjectName("card")
        self.unit = unit
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
        text_layout.setSpacing(2) # Tighter spacing
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #6B7280; font-size: 14px; font-weight: 500;")
        
        self.value_label = QLabel("0")
        self.value_label.setStyleSheet("color: #111827; font-size: 28px; font-weight: bold;")
        
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.value_label)
        
        if self.unit:
            self.unit_label = QLabel(self.unit)
            self.unit_label.setStyleSheet("color: #9CA3AF; font-size: 12px; font-style: italic;")
            text_layout.addWidget(self.unit_label)
            
        layout.addLayout(text_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Animation state
        self.target_value = 0
        self.current_value = 0
        self.display_value = 0
        self.is_float = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_animation)
        self.animations_enabled = True

    def set_value(self, value, animate=True):
        try:
            val = str(value)
            self.is_float = '.' in val
            target = float(val)
        except ValueError:
            # Updates non-numeric text directly
            self.value_label.setText(str(value))
            return

        if not self.animations_enabled or not animate:
             self.value_label.setText(str(value))
             return

        self.target_value = target
        self.current_value = 0 
        
        self.step = target / 20 # 20 steps
        self.timer.start(50) # 50ms * 20 = 1000ms

    def _update_animation(self):
        self.current_value += self.step
        
        if (self.step > 0 and self.current_value >= self.target_value) or \
           (self.step < 0 and self.current_value <= self.target_value):
            self.current_value = self.target_value
            self.timer.stop()
            
        if self.is_float:
            self.value_label.setText(f"{self.current_value:.2f}")
        else:
            self.value_label.setText(str(int(self.current_value)))

    def set_animations_enabled(self, enabled):
        self.animations_enabled = enabled


class SummaryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.animations_enabled = True
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("Summary Statistics")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #111827; margin-bottom: 10px;")
        layout.addWidget(title_label)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        # Create stat cards with web-styled colors and icons
        self.total_card = CardWidget("Total Equipment", "📊", "#1a5490", "rgba(26, 84, 144, 0.1)")
        self.flowrate_card = CardWidget("Avg Flowrate", "💧", "#2ecc71", "rgba(46, 204, 113, 0.1)", "m³/h")
        self.pressure_card = CardWidget("Avg Pressure", "⚙️", "#3B82F6", "rgba(59, 130, 246, 0.1)", "bar")
        self.temperature_card = CardWidget("Avg Temperature", "🌡️", "#EF4444", "rgba(239, 68, 68, 0.1)", "°C")
        
        cards_layout.addWidget(self.total_card)
        cards_layout.addWidget(self.flowrate_card)
        cards_layout.addWidget(self.pressure_card)
        cards_layout.addWidget(self.temperature_card)
        
        layout.addLayout(cards_layout)
        self.setLayout(layout)
    
    def set_animations_enabled(self, enabled):
        self.animations_enabled = enabled
        self.total_card.set_animations_enabled(enabled)
        self.flowrate_card.set_animations_enabled(enabled)
        self.pressure_card.set_animations_enabled(enabled)
        self.temperature_card.set_animations_enabled(enabled)
    
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
        self.total_card.set_value("0", animate=False)
        self.flowrate_card.set_value("0.00", animate=False)
        self.pressure_card.set_value("0.00", animate=False)
        self.temperature_card.set_value("0.00", animate=False)
