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
        self.animations_enabled = True
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create figure with custom layout
        self.figure = Figure(figsize=(10, 10), constrained_layout=True)
        self.canvas = FigureCanvas(self.figure)
        
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.setMinimumHeight(800) # Ensure enough vertical space for the scroll area
        
        self.clear() # Show initial placeholder
        
    def set_animations_enabled(self, enabled):
        self.animations_enabled = enabled
        # No specific animation logic for static matplotlib charts currently
            
    def update_charts(self, summary, raw_data):
        """
        Update charts with new data.
        """
        if not summary:
            return
        
        self.figure.clear()
        
        # Grid layout: 2 rows
        # Row 1: Bar and Pie (side by side, pie gets more width)
        # Row 2: Line Chart (full width)
        gs = self.figure.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1.5])
        
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
        colors_pie = [
            '#FF5733', # Red-Orange
            '#33FF57', # Green
            '#3357FF', # Blue
            '#FF33F6', # Magenta
            '#F6FF33', # Yellow
            '#33FFF6', # Cyan
            '#FF8F33', # Orange
            '#8F33FF', # Purple
            '#FF338F', # Pink
            '#33FF8F', # Mint
            '#581845', # Dark Purple
            '#900C3F'  # Dark Red
        ]
        
        wedges, texts, autotexts = ax2.pie(sizes, autopct='%1.1f%%', startangle=90,
               colors=colors_pie[:len(labels)], textprops={'fontsize': 9}, radius=1.2)
        # Move legend outside but without a massive bounding box that shrinks the chart
        ax2.legend(wedges, labels, title="Equipment Types", loc="center left", bbox_to_anchor=(1, 0.5))
        ax2.set_title('Equipment Distribution', fontsize=12, fontweight='bold', pad=10)
        ax2.axis('equal')
        
        # --- Line Chart (Trends) ---
        # --- Line Chart (Trends) ---
        if raw_data:
            # Downsample if too many points (readability)
            step = 10 if len(raw_data) > 100 else 1
            
            # Create subset lists
            indices = list(range(1, len(raw_data) + 1))[::step]
            flowrates = [d['Flowrate'] for d in raw_data][::step]
            pressures = [d['Pressure'] for d in raw_data][::step]
            temperatures = [d['Temperature'] for d in raw_data][::step]
            
            # Plot with transparency and smaller markers
            ax3.plot(indices, flowrates, label='Flowrate', color='#2ecc71', alpha=0.7, linewidth=1.5, marker='o', markersize=3)
            ax3.plot(indices, pressures, label='Pressure', color='#3B82F6', alpha=0.7, linewidth=1.5, marker='s', markersize=3)
            ax3.plot(indices, temperatures, label='Temperature', color='#EF4444', alpha=0.7, linewidth=1.5, marker='^', markersize=3)
            
            ax3.set_title('Parameter Trends', fontsize=12, fontweight='bold', pad=10)
            ax3.set_xlabel('Equipment Index', fontsize=10)
            ax3.set_ylabel('Value', fontsize=10)
            ax3.legend(loc='upper right', fontsize=9, framealpha=0.9)
            ax3.grid(True, alpha=0.3, linestyle='--')
        
        self.canvas.draw()
    
    def clear(self):
        """
        Clear all charts and show placeholder.
        """
        self.figure.clear()
        
        # Show "No Data" message
        self.figure.text(
            0.5, 0.5, 
            'No data available.\nUpload a CSV file to see visualizations.', 
            ha='center', 
            va='center', 
            fontsize=14, 
            color='#666666'
        )
        
        self.canvas.draw()
