from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent

class UploadWidget(QWidget):
    def __init__(self, upload_callback):
        super().__init__()
        self.upload_callback = upload_callback
        self.selected_file = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Upload CSV File")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Drop zone
        self.drop_zone = QFrame()
        self.drop_zone.setAcceptDrops(True)
        self.drop_zone.setStyleSheet("""
            QFrame {
                border: 3px dashed #ccc;
                border-radius: 12px;
                background: #fafafa;
                min-height: 250px;
            }
            QFrame:hover {
                border-color: #667eea;
                background: #f0f4ff;
            }
        """)
        
        drop_layout = QVBoxLayout(self.drop_zone)
        drop_layout.setAlignment(Qt.AlignCenter)
        
        # Icon
        icon_label = QLabel("📁")
        icon_label.setFont(QFont("Arial", 80))
        icon_label.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(icon_label)
        
        # Selected file label
        self.file_label = QLabel("No file selected")
        self.file_label.setFont(QFont("Arial", 12))
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setStyleSheet("color: #666; margin-top: 20px;")
        drop_layout.addWidget(self.file_label)
        
        # Instructions
        instructions = QLabel("Drag and drop CSV file here\nor")
        instructions.setFont(QFont("Arial", 11))
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("color: #999; margin-top: 10px;")
        drop_layout.addWidget(instructions)
        
        # Browse button
        browse_btn = QPushButton("Browse Files")
        browse_btn.setFont(QFont("Arial", 11))
        browse_btn.setStyleSheet("""
            QPushButton {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: #5568d3;
            }
        """)
        browse_btn.clicked.connect(self.browse_file)
        drop_layout.addWidget(browse_btn, alignment=Qt.AlignCenter)
        
        # Enable drag and drop
        self.drop_zone.dragEnterEvent = self.drag_enter_event
        self.drop_zone.dropEvent = self.drop_event
        
        layout.addWidget(self.drop_zone)
        
        # Upload button
        self.upload_btn = QPushButton("Upload and Process")
        self.upload_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6639a1);
            }
            QPushButton:disabled {
                background: #ccc;
            }
        """)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        layout.addWidget(self.upload_btn)
        
        layout.addStretch()
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            self.set_selected_file(file_path)
    
    def set_selected_file(self, file_path):
        self.selected_file = file_path
        file_name = file_path.split('/')[-1]
        self.file_label.setText(f"Selected: {file_name}")
        self.file_label.setStyleSheet("color: #667eea; font-weight: bold;")
        self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        if self.selected_file:
            try:
                # Disable button during upload
                self.upload_btn.setEnabled(False)
                self.upload_btn.setText("Uploading...")
            

                self.upload_callback(self.selected_file)
            
            except Exception as e:
                print(f"Upload error: {e}")
                QMessageBox.critical(self, "Upload Error", str(e))
            finally:
                self.upload_btn.setEnabled(True)
                self.upload_btn.setText("Upload and Process")
    
    def drag_enter_event(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def drop_event(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files and files[0].endswith('.csv'):
            self.set_selected_file(files[0])
        event.acceptProposedAction()