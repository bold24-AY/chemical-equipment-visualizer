"""
Chart widget for displaying visualizations using Matplotlib.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.animations_enabled = True
        self.chart_elements = {} # Store interactable elements
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Global Font Settings to match Web (Sans-Serif/Arial)
        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['font.size'] = 10
        plt.rcParams['text.color'] = '#333333'
        plt.rcParams['axes.labelcolor'] = '#666666'
        plt.rcParams['xtick.color'] = '#666666'
        plt.rcParams['ytick.color'] = '#666666'
        
        # Create figure with custom layout and WHITE background
        self.figure = Figure(figsize=(10, 10), constrained_layout=True, facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        
        # Connect Hover Event
        self.cid = self.canvas.mpl_connect("motion_notify_event", self.on_hover)
        
        # Enable Mouse Tracking for hover events without clicking
        self.setMouseTracking(True) # Set on Widget
        self.canvas.setMouseTracking(True) # Set on Canvas
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()
        
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.setMinimumHeight(800) 
        
        self.clear() 

    # ... (rest of method)

    def on_hover(self, event):
        """Handle mouse hover events to show tooltips."""
        print(f"Hover: {event.xdata}, {event.ydata} (In Axes: {event.inaxes is not None})")
        if not hasattr(self, 'tooltips'): return
        
        found = False
        if event.inaxes:
            ax = event.inaxes
            tooltip = self.tooltips.get(ax)
            if not tooltip: return

            # --- Bar Chart ---
            if ax == self.ax1:
                for bar, value, category in self.chart_elements.get('bars', []):
                    if bar.contains(event)[0]:
                        tooltip.xy = (bar.get_x() + bar.get_width() / 2, bar.get_height())
                        tooltip.set_text(f"{category}: {value:.2f}")
                        tooltip.set_visible(True)
                        found = True
                        print(f"Hover Bar: {category}")
                        break
            
            # --- Pie Chart ---
            elif ax == self.ax2:
                for wedge, label, value in self.chart_elements.get('wedges', []):
                    if wedge.contains(event)[0]:
                        print(f"Hover Pie: {label}")
                        mid_angle = (wedge.theta2 + wedge.theta1) / 2
                        rad = np.deg2rad(mid_angle)
                        x = 0.7 * np.cos(rad)
                        y = 0.7 * np.sin(rad)
                        tooltip.xy = (x, y)
                        tooltip.set_text(f"{label}: {value}")
                        tooltip.set_visible(True)
                        found = True
                        break

            # --- Line Chart ---
            elif ax == self.ax3:
                line_data = self.chart_elements.get('lines', {})
                if line_data:
                    x_mouse = event.xdata
                    indices = line_data['x']
                    if x_mouse is not None and len(indices) > 0:
                        idx = (np.abs(indices - x_mouse)).argmin()
                        x_point = indices[idx]
                        if abs(x_mouse - x_point) < (indices[-1] - indices[0]) * 0.1: 
                            print(f"Hover Line: {x_point}")
                            tooltip_text = f"Equip #{int(x_point)}\nFlow: {line_data['flow'][idx]:.1f}\nPress: {line_data['press'][idx]:.1f}\nTemp: {line_data['temp'][idx]:.1f}"
                            tooltip.xy = (x_point, line_data['flow'][idx])
                            tooltip.set_text(tooltip_text)
                            tooltip.set_visible(True)
                            found = True
        
    def set_animations_enabled(self, enabled):
        self.animations_enabled = enabled
            
    def update_charts(self, summary, raw_data):
        if not summary:
            return
        
        self.figure.clear()
        self.chart_elements = {} # Reset elements
        
        # Grid layout
        gs = self.figure.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1.5])
        self.ax1 = self.figure.add_subplot(gs[0, 0])      # Bar
        self.ax2 = self.figure.add_subplot(gs[0, 1])      # Pie
        self.ax3 = self.figure.add_subplot(gs[1, :])      # Line
        
        self.tooltips = {}
        for ax in [self.ax1, self.ax2, self.ax3]:
             t = ax.annotate("", xy=(0,0), xytext=(15, 15), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="white", ec="#333333", alpha=0.9),
                            arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                            zorder=100)
             t.set_visible(False)
             self.tooltips[ax] = t
        
        # --- Shared Styling ---
        for ax in [self.ax1, self.ax3]:
            ax.set_facecolor('white')
            ax.grid(axis='y', color='#f0f0f0', linestyle='-', linewidth=1, zorder=0)
            ax.set_axisbelow(True)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#dddddd')
            ax.spines['bottom'].set_color('#dddddd')

        # --- Bar Chart ---
        categories = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            summary['average_flowrate'],
            summary['average_pressure'],
            summary['average_temperature']
        ]
        
        colors = ['#2ecc71', '#3b82f6', '#ef4444']
        
        bars = self.ax1.bar(categories, values, color=colors, alpha=0.9, width=0.6, zorder=3)
        self.chart_elements['bars'] = list(zip(bars, values, categories)) # Store for hover
        
        self.ax1.set_title('Average Parameters', fontsize=12, fontweight='bold', pad=15, color='#333333')
        self.ax1.set_ylabel('Value', fontsize=10)
        
        for bar in bars:
            height = bar.get_height()
            self.ax1.text(bar.get_x() + bar.get_width()/2., height + (height * 0.01),
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color='#444444')
        
        # --- Pie Chart ---
        type_dist = summary['type_distribution']
        labels = list(type_dist.keys())
        sizes = list(type_dist.values())
        colors_pie = [
            '#1a5490', '#2ecc71', '#ef4444', '#f39c12', 
            '#9b59b6', '#3498db', '#1abc9c', '#e74c3c'
        ]
        
        wedges, _ = self.ax2.pie(sizes, startangle=90,
               colors=colors_pie[:len(labels)], 
               radius=1.1)
        self.chart_elements['wedges'] = list(zip(wedges, labels, sizes))
        
        self.ax2.legend(wedges, labels, loc="center left", bbox_to_anchor=(0.95, 0.5), 
                  frameon=False, fontsize=10, labelspacing=0.8, handlelength=1.5, handleheight=1.5) 
        self.ax2.set_title('Equipment Distribution', fontsize=14, fontweight='bold', pad=10, color='#333333')
        
        # --- Line Chart (Trends) ---
        if raw_data:
            step = 10 if len(raw_data) > 100 else 1
            indices = np.array(list(range(1, len(raw_data) + 1))[::step])
            
            # Helper: Catmull-Rom Spline
            def catmull_rom_spline(x, y, num_points=20):
                if len(x) != len(y) or len(x) < 2: return x, y
                t = np.linspace(0, 1, num_points)
                x_interp = []
                y_interp = []
                
                # Pad
                x = np.concatenate(([x[0]], x, [x[-1]]))
                y = np.concatenate(([y[0]], y, [y[-1]]))
                
                for i in range(len(x) - 3):
                    p0, p1, p2, p3 = y[i], y[i+1], y[i+2], y[i+3]
                    t2 = t * t
                    t3 = t2 * t
                    poly = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)
                    x_seg = np.linspace(x[i+1], x[i+2], num_points)
                    x_interp.append(x_seg)
                    y_interp.append(poly)
                return np.concatenate(x_interp), np.concatenate(y_interp)

            def plot_smooth(ax, x, y, label, color):
                if len(x) > 3:
                     x_smooth, y_smooth = catmull_rom_spline(x, y)
                     ax.plot(x_smooth, y_smooth, label=label, color=color, linewidth=2, zorder=3)
                     ax.fill_between(x_smooth, y_smooth, color=color, alpha=0.1, zorder=2)
                else:
                    ax.plot(x, y, label=label, color=color, linewidth=2, zorder=3)
                    ax.fill_between(x, y, color=color, alpha=0.1, zorder=2)

            flowrates = np.array([d['Flowrate'] for d in raw_data][::step])
            pressures = np.array([d['Pressure'] for d in raw_data][::step])
            temperatures = np.array([d['Temperature'] for d in raw_data][::step])
            
            self.chart_elements['lines'] = {
                'x': indices,
                'flow': flowrates,
                'press': pressures,
                'temp': temperatures
            }
            
            plot_smooth(self.ax3, indices, flowrates, 'Flowrate', '#2ecc71')
            plot_smooth(self.ax3, indices, pressures, 'Pressure', '#3b82f6')
            plot_smooth(self.ax3, indices, temperatures, 'Temperature', '#ef4444')
            
            self.ax3.set_title('Parameter Trends', fontsize=12, fontweight='bold', pad=15, color='#333333')
            self.ax3.set_xlabel('Equipment Index', fontsize=10)
            self.ax3.set_ylabel('Value', fontsize=10)
            
            legend = self.ax3.legend(loc='upper right', fontsize=9, frameon=True, facecolor='white', framealpha=1, edgecolor='#eeeeee')
            legend.get_frame().set_linewidth(0) 
            
        self.canvas.draw()
    
    def on_hover(self, event):
        """Handle mouse hover events to show tooltips."""
        # print(f"Hover event: x={event.x}, y={event.y}, inaxes={event.inaxes}") 
        if not hasattr(self, 'tooltips'): return
        
        found = False
        if event.inaxes:
            ax = event.inaxes
            tooltip = self.tooltips.get(ax)
            if not tooltip: return

            # --- Bar Chart ---
            if ax == self.ax1:
                for bar, value, category in self.chart_elements.get('bars', []):
                    # Use contains(event) instead of raw contains_point for better reliability
                    if bar.contains(event)[0]:
                        tooltip.xy = (bar.get_x() + bar.get_width() / 2, bar.get_height())
                        tooltip.set_text(f"{category}: {value:.2f}")
                        tooltip.set_visible(True)
                        found = True
                        break
            
            # --- Pie Chart ---
            elif ax == self.ax2:
                for wedge, label, value in self.chart_elements.get('wedges', []):
                    # Robust hit testing using artist.contains
                    if wedge.contains(event)[0]:
                        mid_angle = (wedge.theta2 + wedge.theta1) / 2
                        rad = np.deg2rad(mid_angle)
                        x = 0.7 * np.cos(rad)
                        y = 0.7 * np.sin(rad)
                        tooltip.xy = (x, y)
                        tooltip.set_text(f"{label}: {value}")
                        tooltip.set_visible(True)
                        found = True
                        break

            # --- Line Chart ---
            elif ax == self.ax3:
                line_data = self.chart_elements.get('lines', {})
                if line_data:
                    x_mouse = event.xdata
                    indices = line_data['x']
                    if x_mouse is not None and len(indices) > 0:
                        idx = (np.abs(indices - x_mouse)).argmin()
                        x_point = indices[idx]
                        if abs(x_mouse - x_point) < (indices[-1] - indices[0]) * 0.1: # Increased tolerance
                            tooltip_text = f"Equip #{int(x_point)}\nFlow: {line_data['flow'][idx]:.1f}\nPress: {line_data['press'][idx]:.1f}\nTemp: {line_data['temp'][idx]:.1f}"
                            tooltip.xy = (x_point, line_data['flow'][idx])
                            tooltip.set_text(tooltip_text)
                            tooltip.set_visible(True)
                            found = True

        # Update visibility
        updated = False
        for ax, t in self.tooltips.items():
            if t.get_visible() != (found and event.inaxes == ax):
                t.set_visible(found and event.inaxes == ax)
                updated = True
        
        if updated:
            self.figure.canvas.draw_idle() 
    
    def clear(self):
        """
        Clear all charts and show placeholder.
        """
        self.figure.clear()
        self.tooltips = {} # Clear tooltips
        
        self.figure.text(
            0.5, 0.5, 
            'No data available.\nUpload a CSV file to see visualizations.', 
            ha='center', 
            va='center', 
            fontsize=14, 
            color='#888888',
            fontweight='normal'
        )
        
        self.canvas.draw()
