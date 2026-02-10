from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SummaryCard(QFrame):
    def __init__(self, icon, title, value):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(self)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 36))
        layout.addWidget(icon_label)
        
        # Content
        content_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 11))
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 24, QFont.Bold))
        value_label.setStyleSheet("color: white;")
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(value_label)
        
        layout.addLayout(content_layout)
        layout.addStretch()

class SummaryWidget(QWidget):
    def __init__(self, pdf_callback):
        super().__init__()
        self.pdf_callback = pdf_callback
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with title and PDF button
        header_layout = QHBoxLayout()
        
        title = QLabel("Summary Statistics")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        pdf_btn = QPushButton("📄 Download PDF Report")
        pdf_btn.setFont(QFont("Arial", 11))
        pdf_btn.setStyleSheet("""
            QPushButton {
                background: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #218838;
            }
        """)
        pdf_btn.clicked.connect(self.pdf_callback)
        header_layout.addWidget(pdf_btn)
        
        main_layout.addLayout(header_layout)
        
        # Filename display
        self.filename_label = QLabel("No dataset loaded")
        self.filename_label.setFont(QFont("Arial", 11))
        self.filename_label.setStyleSheet("""
            padding: 10px;
            background: #f0f4ff;
            border-radius: 6px;
            color: #666;
        """)
        main_layout.addWidget(self.filename_label)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setSpacing(20)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Placeholder
        self.placeholder = QLabel("Upload a CSV file to see summary statistics")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setStyleSheet("color: #999; font-size: 14px; padding: 100px;")
        self.content_layout.addWidget(self.placeholder)
    
    def update_data(self, summary, filename):
        # Clear existing content
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.filename_label.setText(f"Dataset: {filename}")
        self.filename_label.setStyleSheet("""
            padding: 10px;
            background: #f0f4ff;
            border-radius: 6px;
            color: #667eea;
            font-weight: bold;
        """)
        
        # Summary cards grid
        cards_grid = QGridLayout()
        cards_grid.setSpacing(15)
        
        # Card 1: Total Equipment
        card1 = SummaryCard("📊", "Total Equipment", str(summary.get('total_count', 0)))
        cards_grid.addWidget(card1, 0, 0)
        
        # Card 2: Avg Flowrate
        card2 = SummaryCard("💧", "Avg Flowrate", f"{summary.get('avg_flowrate', 0):.2f}")
        cards_grid.addWidget(card2, 0, 1)
        
        # Card 3: Avg Pressure
        card3 = SummaryCard("⚡", "Avg Pressure", f"{summary.get('avg_pressure', 0):.2f}")
        cards_grid.addWidget(card3, 1, 0)
        
        # Card 4: Avg Temperature
        card4 = SummaryCard("🌡️", "Avg Temperature", f"{summary.get('avg_temperature', 0):.2f}")
        cards_grid.addWidget(card4, 1, 1)
        
        self.content_layout.addLayout(cards_grid)
        
        # Equipment type distribution
        type_frame = QFrame()
        type_frame.setStyleSheet("""
            QFrame {
                background: #f8f9ff;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        type_layout = QVBoxLayout(type_frame)
        
        type_title = QLabel("Equipment Type Distribution")
        type_title.setFont(QFont("Arial", 14, QFont.Bold))
        type_title.setStyleSheet("color: #555;")
        type_layout.addWidget(type_title)
        
        type_dist = summary.get('type_distribution', {})
        for eq_type, count in type_dist.items():
            item_frame = QFrame()
            item_frame.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 6px;
                    padding: 10px;
                    border-left: 4px solid #667eea;
                }
            """)
            
            item_layout = QHBoxLayout(item_frame)
            
            name_label = QLabel(eq_type)
            name_label.setFont(QFont("Arial", 11, QFont.Bold))
            name_label.setStyleSheet("color: #333;")
            
            count_label = QLabel(f"{count} units")
            count_label.setFont(QFont("Arial", 11))
            count_label.setStyleSheet("color: #667eea; font-weight: 500;")
            
            item_layout.addWidget(name_label)
            item_layout.addStretch()
            item_layout.addWidget(count_label)
            
            type_layout.addWidget(item_frame)
        
        self.content_layout.addWidget(type_frame)
        self.content_layout.addStretch()