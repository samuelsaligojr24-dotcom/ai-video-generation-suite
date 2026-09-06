# Desktop App using PyQt5
# Standalone application for video generation

import sys
import json
import os
from pathlib import Path
from datetime import datetime
import threading
from typing import Callable, Optional

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QTextEdit, QComboBox, QSpinBox, QPushButton,
        QProgressBar, QTableWidget, QTableWidgetItem, QFileDialog,
        QMessageBox, QTabWidget, QStatusBar, QGroupBox
    )
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
    from PyQt5.QtGui import QColor, QFont, QIcon
    from PyQt5.QtWidgets import QStyle
except ImportError:
    print("PyQt5 not installed. Install with: pip install PyQt5")
    sys.exit(1)

import torch


class WorkerSignals(QObject):
    """Signals for worker thread"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)  # job_id
    error = pyqtSignal(str)


class VideoGeneratorApp(QMainWindow):
    """Main Desktop Application Window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 AI Video Generator - Desktop")
        self.setGeometry(100, 100, 1200, 800)
        self.jobs = {}
        self.current_job_id = None
        
        # Set application style
        self.setStyleSheet(self.get_stylesheet())
        
        # Create UI
        self.create_ui()
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.update_status("Ready")
        
        # Timer for job updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_jobs_display)
        self.update_timer.start(1000)
    
    def create_ui(self):
        """Create user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        # Left panel - Generator
        left_panel = self.create_generator_panel()
        
        # Right panel - Jobs
        right_panel = self.create_jobs_panel()
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        central_widget.setLayout(main_layout)
    
    def create_generator_panel(self) -> QGroupBox:
        """Create video generation panel"""
        group = QGroupBox("Generate Video")
        layout = QVBoxLayout()
        
        # Tool selection
        layout.addWidget(QLabel("Select AI Tool:"))
        self.tool_combo = QComboBox()
        self.tool_combo.addItems([
            "LTX-Video (Fastest) ⚡",
            "Wan 2.2 (Best Quality) ✨",
            "HunyuanVideo (Cinematic) 🎥",
            "Mochi 1 (Flexible) 🎨",
            "CogVideoX (Image Animation) 📷",
            "AnimateDiff (Low VRAM) 💻",
            "Open-Sora (Research) 🔬",
            "Stable Video (Versatile) 🎭",
            "VideoCrafter (Artistic) 🖼️",
            "ModelScope T2V (Balanced) ⚖️"
        ])
        layout.addWidget(self.tool_combo)
        
        # Prompt input
        layout.addWidget(QLabel("Video Description (Prompt):"))
        self.prompt_text = QTextEdit()
        self.prompt_text.setPlaceholderText("Describe the video you want to generate...")
        self.prompt_text.setMaximumHeight(100)
        layout.addWidget(self.prompt_text)
        
        # Resolution
        layout.addWidget(QLabel("Resolution:"))
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["512x384 (Fast)", "768x576 (Balanced)", "1280x720 (HD)"])
        self.resolution_combo.setCurrentIndex(1)
        layout.addWidget(self.resolution_combo)
        
        # Duration
        layout.addWidget(QLabel("Duration (seconds):"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setValue(4)
        self.duration_spin.setRange(1, 30)
        layout.addWidget(self.duration_spin)
        
        # Generate button
        self.generate_btn = QPushButton("🚀 Generate Video")
        self.generate_btn.clicked.connect(self.generate_video)
        self.generate_btn.setMinimumHeight(40)
        layout.addWidget(self.generate_btn)
        
        # Progress bar
        layout.addWidget(QLabel("Progress:"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # System info
        layout.addWidget(QLabel("System Information:"))
        self.system_info_label = QLabel()
        self.update_system_info()
        layout.addWidget(self.system_info_label)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
    
    def create_jobs_panel(self) -> QGroupBox:
        """Create jobs display panel"""
        group = QGroupBox("Generation History")
        layout = QVBoxLayout()
        
        # Jobs table
        self.jobs_table = QTableWidget()
        self.jobs_table.setColumnCount(5)
        self.jobs_table.setHorizontalHeaderLabels(["Tool", "Prompt", "Status", "Progress", "Actions"])
        self.jobs_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.jobs_table)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.update_jobs_display)
        btn_layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("💾 Export Jobs")
        export_btn.clicked.connect(self.export_jobs)
        btn_layout.addWidget(export_btn)
        
        clear_btn = QPushButton("🗑️ Clear History")
        clear_btn.clicked.connect(self.clear_history)
        btn_layout.addWidget(clear_btn)
        
        layout.addLayout(btn_layout)
        
        group.setLayout(layout)
        return group
    
    def generate_video(self):
        """Generate video"""
        prompt = self.prompt_text.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Error", "Please enter a video description")
            return
        
        tool = self.tool_combo.currentText().split(" ")[0].lower()
        resolution = self.resolution_combo.currentText().split(" ")[0]
        duration = self.duration_spin.value()
        
        # Create job
        import uuid
        job_id = str(uuid.uuid4())
        
        self.jobs[job_id] = {
            'id': job_id,
            'tool': tool,
            'prompt': prompt,
            'resolution': resolution,
            'duration': duration,
            'status': 'processing',
            'progress': 0,
            'start_time': datetime.now().isoformat()
        }
        
        self.current_job_id = job_id
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("⏳ Generating...")
        
        # Simulate generation (in real app, call actual generator)
        self.simulate_generation(job_id)
        
        self.update_status(f"Generating video: {prompt[:50]}...")
    
    def simulate_generation(self, job_id):
        """Simulate video generation in background"""
        def worker():
            try:
                for i in range(0, 101, 10):
                    self.jobs[job_id]['progress'] = i
                    self.progress_bar.setValue(i)
                    QApplication.processEvents()
                    threading.Event().wait(0.5)
                
                self.jobs[job_id]['status'] = 'completed'
                self.jobs[job_id]['end_time'] = datetime.now().isoformat()
                self.jobs[job_id]['output'] = f"outputs/video_{job_id}.mp4"
                
                self.generate_btn.setEnabled(True)
                self.generate_btn.setText("🚀 Generate Video")
                self.update_status("Ready")
                self.prompt_text.clear()
                
                QMessageBox.information(self, "Success", "Video generation completed!")
            
            except Exception as e:
                self.jobs[job_id]['status'] = 'failed'
                self.jobs[job_id]['error'] = str(e)
                self.generate_btn.setEnabled(True)
                self.generate_btn.setText("🚀 Generate Video")
                QMessageBox.critical(self, "Error", f"Generation failed: {str(e)}")
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def update_jobs_display(self):
        """Update jobs table display"""
        self.jobs_table.setRowCount(len(self.jobs))
        
        for row, (job_id, job) in enumerate(self.jobs.items()):
            tool_item = QTableWidgetItem(job['tool'])
            prompt_item = QTableWidgetItem(job['prompt'][:50] + "...")
            status_item = QTableWidgetItem(job['status'].upper())
            progress_item = QTableWidgetItem(f"{job.get('progress', 0)}%")
            
            # Color status
            if job['status'] == 'completed':
                status_item.setForeground(QColor(40, 167, 69))
            elif job['status'] == 'processing':
                status_item.setForeground(QColor(0, 123, 255))
            elif job['status'] == 'failed':
                status_item.setForeground(QColor(220, 53, 69))
            
            self.jobs_table.setItem(row, 0, tool_item)
            self.jobs_table.setItem(row, 1, prompt_item)
            self.jobs_table.setItem(row, 2, status_item)
            self.jobs_table.setItem(row, 3, progress_item)
            
            # Download button for completed jobs
            if job['status'] == 'completed':
                download_btn = QPushButton("⬇️ Download")
                download_btn.clicked.connect(lambda checked, jid=job_id: self.download_video(jid))
                self.jobs_table.setCellWidget(row, 4, download_btn)
    
    def download_video(self, job_id):
        """Download generated video"""
        job = self.jobs.get(job_id)
        if not job:
            QMessageBox.warning(self, "Error", "Job not found")
            return
        
        if job['status'] != 'completed':
            QMessageBox.warning(self, "Error", "Video not ready")
            return
        
        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(
            self,
            "Save Video",
            f"video_{job_id}.mp4",
            "Video Files (*.mp4)"
        )
        
        if save_path:
            try:
                import shutil
                shutil.copy(job['output'], save_path)
                QMessageBox.information(self, "Success", f"Video saved to {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to download: {str(e)}")
    
    def export_jobs(self):
        """Export jobs history to JSON"""
        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(
            self,
            "Export Jobs",
            "jobs_history.json",
            "JSON Files (*.json)"
        )
        
        if save_path:
            try:
                with open(save_path, 'w') as f:
                    json.dump(self.jobs, f, indent=2)
                QMessageBox.information(self, "Success", f"Jobs exported to {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def clear_history(self):
        """Clear job history"""
        reply = QMessageBox.question(
            self,
            "Confirm",
            "Clear all job history?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.jobs.clear()
            self.update_jobs_display()
            self.update_status("Ready")
    
    def update_system_info(self):
        """Update system information display"""
        gpu_info = "✅ GPU Available" if torch.cuda.is_available() else "❌ CPU Only"
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            gpu_info += f"\n{gpu_name} ({gpu_memory:.1f}GB)"
        
        info_text = f"""GPU: {gpu_info}
PyTorch: {torch.__version__}
CUDA: {'Enabled' if torch.cuda.is_available() else 'Disabled'}"""
        
        self.system_info_label.setText(info_text)
    
    def update_status(self, message: str):
        """Update status bar"""
        self.statusBar.showMessage(message)
    
    @staticmethod
    def get_stylesheet() -> str:
        """Get application stylesheet"""
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                color: #333;
                border: 2px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QLabel {
                color: #333;
                font-weight: 500;
            }
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #764ba2;
            }
            QPushButton:pressed {
                background-color: #5568d3;
            }
            QComboBox, QSpinBox, QTextEdit, QLineEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
                color: #333;
            }
            QComboBox:focus, QSpinBox:focus, QTextEdit:focus, QLineEdit:focus {
                border: 2px solid #667eea;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 5px;
                text-align: center;
                color: #333;
            }
            QProgressBar::chunk {
                background-color: #667eea;
                border-radius: 3px;
            }
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #e0e0e0;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #ddd;
            }
        """


def main():
    """Run desktop application"""
    print("""
    ╔════════════════════════════════════════════╗
    ║  🎬 AI Video Generator - Desktop App      ║
    ║     Free & Unlimited Video Generation     ║
    ╚════════════════════════════════════════════╝
    """)
    
    app = QApplication(sys.argv)
    app.setApplicationName("AI Video Generator")
    
    window = VideoGeneratorApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
