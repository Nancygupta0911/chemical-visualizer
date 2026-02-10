from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        # Increased figure size for better visibility
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='white')
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(500)  # Set minimum height for each chart

class ChartsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Compact header with white background
        header = QWidget()
        header.setStyleSheet("""
            background: white; 
            border-bottom: 2px solid #bdc3c7;
        """)
        header.setMaximumHeight(60)  # Limit header height
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        title = QLabel("📊 Data Visualization")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; border: none;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        main_layout.addWidget(header)
        
        # Scroll area for charts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background: #ecf0f1; 
            }
            QScrollBar:vertical {
                border: none;
                background: #bdc3c7;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #7f8c8d;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #95a5a6;
            }
        """)
        
        charts_container = QWidget()
        charts_container.setStyleSheet("background: #ecf0f1;")
        self.charts_layout = QVBoxLayout(charts_container)
        self.charts_layout.setSpacing(30)  # Increased spacing between charts
        self.charts_layout.setContentsMargins(20, 20, 20, 20)
        
        scroll.setWidget(charts_container)
        main_layout.addWidget(scroll)
        
        # Placeholder
        self.show_placeholder()
    
    def show_placeholder(self):
        """Display placeholder when no data is available"""
        placeholder_widget = QWidget()
        placeholder_widget.setMinimumHeight(400)
        placeholder_layout = QVBoxLayout(placeholder_widget)
        placeholder_layout.setAlignment(Qt.AlignCenter)
        
        icon = QLabel("📈")
        icon.setFont(QFont("Segoe UI", 64))
        icon.setAlignment(Qt.AlignCenter)
        
        text = QLabel("No data to visualize")
        text.setFont(QFont("Segoe UI", 18, QFont.Bold))
        text.setStyleSheet("color: #7f8c8d; margin-top: 20px;")
        text.setAlignment(Qt.AlignCenter)
        
        subtext = QLabel("Please upload a CSV file to see beautiful charts")
        subtext.setFont(QFont("Segoe UI", 13))
        subtext.setStyleSheet("color: #95a5a6; margin-top: 10px;")
        subtext.setAlignment(Qt.AlignCenter)
        
        placeholder_layout.addStretch()
        placeholder_layout.addWidget(icon)
        placeholder_layout.addWidget(text)
        placeholder_layout.addWidget(subtext)
        placeholder_layout.addStretch()
        
        self.charts_layout.addWidget(placeholder_widget)
    
    def update_charts(self, data, summary):
        """Update charts with new data"""
        # Clear existing charts
        while self.charts_layout.count():
            child = self.charts_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not data or not summary:
            self.show_placeholder()
            return
        
        try:
            # Chart 1: Equipment Type Distribution (Pie Chart)
            type_chart = self.create_type_distribution_chart(summary)
            self.charts_layout.addWidget(type_chart)
            
            # Chart 2: Average Parameters (Bar Chart)
            avg_chart = self.create_average_params_chart(summary)
            self.charts_layout.addWidget(avg_chart)
            
            # Chart 3: Parameter Ranges (Grouped Bar Chart)
            range_chart = self.create_parameter_ranges_chart(summary)
            self.charts_layout.addWidget(range_chart)
            
            self.charts_layout.addStretch()
            
        except Exception as e:
            error_label = QLabel(f"❌ Error creating charts: {str(e)}")
            error_label.setStyleSheet("color: #e74c3c; padding: 40px; font-size: 14px;")
            error_label.setAlignment(Qt.AlignCenter)
            self.charts_layout.addWidget(error_label)
    
    def create_chart_container(self, title_text, icon=""):
        """Create a styled container for charts with better spacing"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: 2px solid #bdc3c7;
            }
        """)
        container.setFrameShape(QFrame.StyledPanel)
        container.setMinimumHeight(550)  # Fixed minimum height for each chart
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Title with icon
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        if icon:
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Segoe UI", 18))
            title_layout.addWidget(icon_label)
        
        title = QLabel(title_text)
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; border: none;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addWidget(title_widget)
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background: #bdc3c7; max-height: 2px;")
        layout.addWidget(line)
        
        return container, layout
    
    def create_type_distribution_chart(self, summary):
        """Create pie chart for equipment type distribution"""
        widget, layout = self.create_chart_container("Equipment Type Distribution", "🔧")
        
        # Chart with larger size
        canvas = ChartCanvas(widget, width=10, height=7)
        
        type_dist = summary.get('type_distribution', {})
        if not type_dist:
            return widget
            
        labels = list(type_dist.keys())
        sizes = list(type_dist.values())
        
        # Professional color palette
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', 
                  '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#d35400']
        
        # Create pie chart with better styling
        wedges, texts, autotexts = canvas.axes.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors[:len(labels)], 
            startangle=45,
            textprops={'fontsize': 12, 'weight': 'bold'},
            explode=[0.08] * len(labels),  # More separation
            shadow=True,
            radius=1.0
        )
        
        # Style percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_weight('bold')
        
        # Style labels
        for text in texts:
            text.set_fontsize(12)
            text.set_weight('bold')
        
        canvas.axes.axis('equal')
        
        # Add padding around the chart
        canvas.fig.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05)
        canvas.draw()
        
        layout.addWidget(canvas)
        return widget
    
    def create_average_params_chart(self, summary):
        """Create bar chart for average parameters"""
        widget, layout = self.create_chart_container("Average Parameters", "📊")
        
        # Chart with larger size
        canvas = ChartCanvas(widget, width=10, height=7)
        
        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            summary.get('avg_flowrate', 0),
            summary.get('avg_pressure', 0),
            summary.get('avg_temperature', 0)
        ]
        
        colors = ['#3498db', '#e74c3c', '#2ecc71']
        
        bars = canvas.axes.bar(
            params, 
            values, 
            color=colors, 
            alpha=0.85,
            edgecolor='#2c3e50',
            linewidth=2.5,
            width=0.5
        )
        
        # Styling
        canvas.axes.set_ylabel('Average Value', fontsize=14, fontweight='bold', color='#2c3e50', labelpad=10)
        canvas.axes.set_xlabel('Parameters', fontsize=14, fontweight='bold', color='#2c3e50', labelpad=10)
        canvas.axes.spines['top'].set_visible(False)
        canvas.axes.spines['right'].set_visible(False)
        canvas.axes.spines['left'].set_linewidth(2)
        canvas.axes.spines['bottom'].set_linewidth(2)
        canvas.axes.spines['left'].set_color('#7f8c8d')
        canvas.axes.spines['bottom'].set_color('#7f8c8d')
        canvas.axes.tick_params(colors='#2c3e50', labelsize=12, width=2, length=6)
        canvas.axes.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            canvas.axes.text(
                bar.get_x() + bar.get_width()/2., 
                height,
                f'{height:.2f}',
                ha='center', 
                va='bottom', 
                fontweight='bold',
                fontsize=13,
                color='#2c3e50',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='gray', alpha=0.8)
            )
        
        # Add padding
        canvas.fig.subplots_adjust(left=0.12, right=0.95, top=0.95, bottom=0.12)
        canvas.draw()
        
        layout.addWidget(canvas)
        return widget
    
    def create_parameter_ranges_chart(self, summary):
        """Create grouped bar chart for parameter ranges"""
        widget, layout = self.create_chart_container("Parameter Ranges (Min vs Max)", "📏")
        
        # Chart with larger size
        canvas = ChartCanvas(widget, width=10, height=7)
        
        params = ['Flowrate', 'Pressure', 'Temperature']
        min_values = [
            summary.get('min_flowrate', 0),
            summary.get('min_pressure', 0),
            summary.get('min_temperature', 0)
        ]
        max_values = [
            summary.get('max_flowrate', 0),
            summary.get('max_pressure', 0),
            summary.get('max_temperature', 0)
        ]
        
        x = list(range(len(params)))
        width = 0.35
        
        bars1 = canvas.axes.bar(
            [i - width/2 for i in x], 
            min_values, 
            width,
            label='Minimum', 
            color='#3498db', 
            alpha=0.85,
            edgecolor='#2c3e50',
            linewidth=2
        )
        
        bars2 = canvas.axes.bar(
            [i + width/2 for i in x], 
            max_values, 
            width,
            label='Maximum', 
            color='#e74c3c', 
            alpha=0.85,
            edgecolor='#2c3e50',
            linewidth=2
        )
        
        # Styling
        canvas.axes.set_ylabel('Value', fontsize=14, fontweight='bold', color='#2c3e50', labelpad=10)
        canvas.axes.set_xlabel('Parameters', fontsize=14, fontweight='bold', color='#2c3e50', labelpad=10)
        canvas.axes.set_xticks(x)
        canvas.axes.set_xticklabels(params, fontsize=13, fontweight='bold')
        canvas.axes.spines['top'].set_visible(False)
        canvas.axes.spines['right'].set_visible(False)
        canvas.axes.spines['left'].set_linewidth(2)
        canvas.axes.spines['bottom'].set_linewidth(2)
        canvas.axes.spines['left'].set_color('#7f8c8d')
        canvas.axes.spines['bottom'].set_color('#7f8c8d')
        canvas.axes.tick_params(colors='#2c3e50', labelsize=12, width=2, length=6)
        canvas.axes.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1.2)
        
        # Legend with better styling
        canvas.axes.legend(
            loc='upper left',
            frameon=True,
            fancybox=True,
            shadow=True,
            fontsize=12,
            edgecolor='#7f8c8d',
            facecolor='white'
        )
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                canvas.axes.text(
                    bar.get_x() + bar.get_width()/2., 
                    height,
                    f'{height:.1f}',
                    ha='center', 
                    va='bottom', 
                    fontsize=11,
                    fontweight='bold',
                    color='#2c3e50',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.7)
                )
        
        # Add padding
        canvas.fig.subplots_adjust(left=0.12, right=0.95, top=0.95, bottom=0.12)
        canvas.draw()
        
        layout.addWidget(canvas)
        return widget