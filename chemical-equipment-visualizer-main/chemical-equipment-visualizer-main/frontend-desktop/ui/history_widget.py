from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                             QHBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime

class HistoryItem(QFrame):
    def __init__(self, dataset, callback):
        super().__init__()
        self.dataset = dataset
        self.callback = callback
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QFrame {
                background: #f8f9ff;
                border: 2px solid transparent;
                border-radius: 10px;
                padding: 15px;
            }
            QFrame:hover {
                background: #f0f4ff;
                border-color: #667eea;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        
        filename_label = QLabel(f"📁 {self.dataset['filename']}")
        filename_label.setFont(QFont("Arial", 12, QFont.Bold))
        filename_label.setStyleSheet("color: #333;")
        header_layout.addWidget(filename_label)
        
        layout.addLayout(header_layout)
        
        # Meta info
        meta_layout = QHBoxLayout()
        
        # Format upload date
        upload_date = self.dataset.get('upload_date', '')
        if upload_date:
            try:
                dt = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                date_str = dt.strftime('%b %d, %Y %I:%M %p')
            except:
                date_str = upload_date
        else:
            date_str = 'Unknown'
        
        date_label = QLabel(f"🕒 {date_str}")
        date_label.setFont(QFont("Arial", 10))
        date_label.setStyleSheet("color: #666;")
        meta_layout.addWidget(date_label)
        
        meta_layout.addStretch()
        
        count = self.dataset.get('summary', {}).get('total_count', 0)
        count_label = QLabel(f"📊 {count} items")
        count_label.setFont(QFont("Arial", 10))
        count_label.setStyleSheet("color: #666;")
        meta_layout.addWidget(count_label)
        
        layout.addLayout(meta_layout)
    
    def mousePressEvent(self, event):
        self.callback(self.dataset['id'])

class HistoryWidget(QWidget):
    def __init__(self, select_callback):
        super().__init__()
        self.select_callback = select_callback
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Recent Datasets (Last 5)")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(title)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(10)
        
        scroll.setWidget(self.content_widget)
        main_layout.addWidget(scroll)
        
        # Placeholder
        self.placeholder = QLabel("No datasets uploaded yet.\nUpload a CSV to get started!")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setStyleSheet("color: #999; font-size: 14px; padding: 100px;")
        self.content_layout.addWidget(self.placeholder)
    
    def update_datasets(self, datasets):
        # Clear existing items
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not datasets:
            self.placeholder = QLabel("No datasets uploaded yet.\nUpload a CSV to get started!")
            self.placeholder.setAlignment(Qt.AlignCenter)
            self.placeholder.setStyleSheet("color: #999; font-size: 14px; padding: 100px;")
            self.content_layout.addWidget(self.placeholder)
            return
        
        # Add dataset items
        for dataset in datasets:
            item = HistoryItem(dataset, self.select_callback)
            self.content_layout.addWidget(item)
        
        self.content_layout.addStretch()