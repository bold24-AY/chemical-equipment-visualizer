"""
Chart widget for displaying visualizations using Matplotlib.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Apply style
plt.style.use('ggplot')

class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create figure with custom layout
        self.figure = Figure(figsize=(10, 10), constrained_layout=True)
        self.canvas = FigureCanvas(self.figure)
        
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.setMinimumHeight(800) # Ensure enough vertical space for the scroll area
    
    def update_charts(self, summary, raw_data):
        """
        Update charts with new data.
        """
        if not summary:
            return
        
        self.figure.clear()
        
        # Grid layout: 2 rows, 2 columns
        gs = self.figure.add_gridspec(2, 2, height_ratios=[1, 1])
        
        # Ax1: Bar Chart (Top Left)
        ax1 = self.figure.add_subplot(gs[0, 0])
        
        # Ax2: Pie Chart (Top Right)
        ax2 = self.figure.add_subplot(gs[0, 1])
        
        # Ax3: Line Chart (Bottom, spanning both columns)
        ax3 = self.figure.add_subplot(gs[1, :])
        
        # --- Bar Chart ---
        categories = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            summary['average_flowrate'],
            summary['average_pressure'],
            summary['average_temperature']
        ]
        colors = ['#2ecc71', '#3B82F6', '#EF4444']
        
        bars = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax1.set_title('Average Parameters', fontsize=12, fontweight='bold', pad=10)
        ax1.set_ylabel('Value', fontsize=10)
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # --- Pie Chart ---
        type_dist = summary['type_distribution']
        labels = list(type_dist.keys())
        sizes = list(type_dist.values())
        colors_pie = ['#1a5490', '#2ecc71', '#EF4444', '#f39c12', '#9b59b6', '#3498db']
        
        wedges, texts, autotexts = ax2.pie(sizes, autopct='%1.1f%%', startangle=90,
               colors=colors_pie[:len(labels)], textprops={'fontsize': 9})
        ax2.legend(wedges, labels, title="Equipment Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        ax2.set_title('Equipment Distribution', fontsize=12, fontweight='bold', pad=10)
        ax2.axis('equal')
        
        # --- Line Chart (Trends) ---
        if raw_data:
            indices = range(1, len(raw_data) + 1)
            flowrates = [d['Flowrate'] for d in raw_data]
            pressures = [d['Pressure'] for d in raw_data]
            temperatures = [d['Temperature'] for d in raw_data]
            
            ax3.plot(indices, flowrates, label='Flowrate', color='#2ecc71', linewidth=2, marker='o', markersize=4)
            ax3.plot(indices, pressures, label='Pressure', color='#3B82F6', linewidth=2, marker='s', markersize=4)
            ax3.plot(indices, temperatures, label='Temperature', color='#EF4444', linewidth=2, marker='^', markersize=4)
            
            ax3.set_title('Parameter Trends', fontsize=12, fontweight='bold', pad=10)
            ax3.set_xlabel('Equipment Index', fontsize=10)
            ax3.set_ylabel('Value', fontsize=10)
            ax3.legend(loc='upper right', fontsize=9, framealpha=0.9)
            ax3.grid(True, alpha=0.3, linestyle='--')
        
        self.canvas.draw()
    
    def clear(self):
        """
        Clear all charts.
        """
        self.figure.clear()
        self.canvas.draw()
