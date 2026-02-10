from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QMessageBox, 
                             QTabWidget, QStatusBar, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import APIClient
from ui.upload_widget import UploadWidget
from ui.table_widget import TableWidget
from ui.charts_widget import ChartsWidget
from ui.summary_widget import SummaryWidget
from ui.history_widget import HistoryWidget

class UploadThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        try:
            result = self.api_client.upload_csv(self.file_path)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_dataset = None
        self.init_ui()
        self.check_backend_connection()
        
    def init_ui(self):
        self.setWindowTitle("⚗️ Chemical Equipment Parameter Visualizer - Desktop")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set color scheme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 244, 255))
        self.setPalette(palette)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #667eea;
                border-radius: 8px;
                background: white;
            }
            QTabBar::tab {
                background: #e8ecff;
                color: #333;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: #667eea;
                color: white;
            }
        """)
        
        # Upload tab
        self.upload_widget = UploadWidget(self.handle_upload)
        self.tabs.addTab(self.upload_widget, "📁 Upload")
        
        # Summary tab
        self.summary_widget = SummaryWidget(self.handle_download_pdf)
        self.tabs.addTab(self.summary_widget, "📊 Summary")
        
        # Charts tab
        self.charts_widget = ChartsWidget()
        self.tabs.addTab(self.charts_widget, "📈 Charts")
        
        # Data table tab
        self.table_widget = TableWidget()
        self.tabs.addTab(self.table_widget, "📋 Data Table")
        
        # History tab
        self.history_widget = HistoryWidget(self.handle_select_dataset)
        self.tabs.addTab(self.history_widget, "🕒 History")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def create_header(self):
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(header_frame)
        
        title = QLabel("⚗️ Chemical Equipment Parameter Visualizer")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Desktop Application")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 16px;")
        subtitle.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        return header_frame
    
    def check_backend_connection(self):
        if self.api_client.health_check():
            self.status_bar.showMessage("✓ Connected to backend")
            self.load_datasets()
        else:
            QMessageBox.warning(
                self,
                "Backend Connection",
                "Cannot connect to backend server.\n"
                "Please ensure Django backend is running on http://localhost:8000"
            )
            self.status_bar.showMessage("✗ Backend not connected")
    
    def handle_upload(self, file_path):
        self.status_bar.showMessage("Uploading...")
        
        self.upload_thread = UploadThread(self.api_client, file_path)
        self.upload_thread.finished.connect(self.on_upload_success)
        self.upload_thread.error.connect(self.on_upload_error)
        self.upload_thread.start()
    
    def on_upload_success(self, dataset):
        self.current_dataset = dataset
        self.update_all_widgets()
        self.load_datasets()
        self.status_bar.showMessage("✓ Upload successful!")
        QMessageBox.information(self, "Success", "CSV file uploaded and processed successfully!")
    
    def on_upload_error(self, error_msg):
        self.status_bar.showMessage("✗ Upload failed")
        QMessageBox.critical(self, "Upload Error", f"Failed to upload file:\n{error_msg}")
    
    def load_datasets(self):
        try:
            datasets = self.api_client.get_datasets()
            self.history_widget.update_datasets(datasets)
        except Exception as e:
            print(f"Error loading datasets: {e}")
    
    def handle_select_dataset(self, dataset_id):
        try:
            dataset = self.api_client.get_dataset(dataset_id)
            self.current_dataset = dataset
            self.update_all_widgets()
            self.status_bar.showMessage(f"✓ Loaded dataset: {dataset['filename']}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load dataset:\n{str(e)}")
    
    def update_all_widgets(self):
        if self.current_dataset:
            self.summary_widget.update_data(
                self.current_dataset['summary'],
                self.current_dataset['filename']
            )
            self.charts_widget.update_charts(
                self.current_dataset['data'],
                self.current_dataset['summary']
            )
            self.table_widget.update_table(self.current_dataset['data'])
    
    def handle_download_pdf(self):
        if not self.current_dataset:
            QMessageBox.warning(self, "Warning", "No dataset selected")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            f"equipment_report_{self.current_dataset['id']}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                self.api_client.download_pdf(self.current_dataset['id'], file_path)
                QMessageBox.information(self, "Success", "PDF report downloaded successfully!")
                self.status_bar.showMessage(f"✓ PDF saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to download PDF:\n{str(e)}")