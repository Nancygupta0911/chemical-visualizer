from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QLabel, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Equipment Data")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        # Info label
        self.info_label = QLabel("No data loaded")
        self.info_label.setFont(QFont("Arial", 10))
        self.info_label.setStyleSheet("color: #666;")
        layout.addWidget(self.info_label)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        
        # Style table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9ff;
                selection-background-color: #667eea;
                gridline-color: #e0e0e0;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #667eea;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.table)
    
    def update_table(self, data):
        self.table.setRowCount(0)
        
        if not data:
            self.info_label.setText("No data to display")
            return
        
        self.info_label.setText(f"Showing {len(data)} equipment entries")
        
        self.table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            # Equipment Name
            name_item = QTableWidgetItem(str(row_data.get('Equipment Name', '')))
            self.table.setItem(row_idx, 0, name_item)
            
            # Type
            type_item = QTableWidgetItem(str(row_data.get('Type', '')))
            self.table.setItem(row_idx, 1, type_item)
            
            # Flowrate
            flowrate = row_data.get('Flowrate', 0)
            flowrate_item = QTableWidgetItem(f"{float(flowrate):.2f}" if flowrate else "N/A")
            flowrate_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 2, flowrate_item)
            
            # Pressure
            pressure = row_data.get('Pressure', 0)
            pressure_item = QTableWidgetItem(f"{float(pressure):.2f}" if pressure else "N/A")
            pressure_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 3, pressure_item)
            
            # Temperature
            temperature = row_data.get('Temperature', 0)
            temp_item = QTableWidgetItem(f"{float(temperature):.2f}" if temperature else "N/A")
            temp_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 4, temp_item)