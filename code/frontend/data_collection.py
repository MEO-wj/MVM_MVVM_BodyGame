"""
Created by Taizhou CHEN
Shantou University 
tzchen@stu.edu.cn

"""

import sys
import cv2
import time
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, \
    QGroupBox, QPushButton, QVBoxLayout, QWidget, QHBoxLayout


folder = sys.argv[1] if len(sys.argv) > 1 else "dataset"

DATA_DIR = Path(__file__).resolve().parent/folder
LABELS = ["Fist", "Plam Up", "Plam Down"]
CAPTURE_INTERVAL = 0.5

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Collection")
        self.resize(960, 540)
        self.is_recording = False
        self.last_capture = 0
        self.save_frame_count = 0

        self.preview = QLabel("Opening Camera...")
        self.preview.setMinimumSize(480, 360)
        self.preview.setStyleSheet("background: #202124; color: white; border-radius: 8px;")

        self.control_group = QGroupBox("Recording Control")
        self.label_box = QComboBox()
        self.label_box.addItems(LABELS)
        self.record_btn = QPushButton("Start Recording")
        self.count_label = QLabel(f"{self.save_frame_count} frames have been saved.")

        self.control_layout = QVBoxLayout(self.control_group)
        self.control_layout.addWidget(self.label_box)
        self.control_layout.addWidget(self.record_btn)
        self.control_layout.addWidget(self.count_label)

        self.path_label = QLabel(f"Save position: \n{DATA_DIR}")
        self.path_label.setWordWrap(True)

        self.sidebar_widget = QWidget()
        self.sidebar = QVBoxLayout()
        self.sidebar_widget.setLayout(self.sidebar)

        self.sidebar.addWidget(self.control_group)
        self.sidebar.addStretch()
        self.sidebar.addWidget(self.path_label)
        
        self.central = QWidget()
        self.layout = QHBoxLayout()
        self.central.setLayout(self.layout)

        self.layout.addWidget(self.preview, stretch=2)
        self.layout.addWidget(self.sidebar_widget, stretch=1)
        self.setCentralWidget(self.central)

        self.record_btn.clicked.connect(self.toggle_recording)

        self.record_shortcut = QShortcut(QKeySequence("R"), self)
        self.record_shortcut.activated.connect(self.toggle_recording)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.open_camera()

    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.record_btn.setText("Start Recording")
        else:
            self.is_recording = True
            self.label = self.label_box.currentIndex()
            self.last_capture = 0
            self.record_btn.setText("Stop Recording")

    def open_camera(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("ERROR: Cannot Open Camera.")
            return
        self.timer.start(33)   

    def update_frame(self):
        ok, frame = self.camera.read()
        if not ok:
            self.frame = None
            self.read_failures += 1
            if self.read_failures >= 30:
                print("ERROR: Failed to Read Frames")
            return
        self.frame = cv2.flip(frame, 1)
        self.read_failures = 0
        display = self.frame.copy()

        # hand area
        x, y, size, _ = self.hand_area()
        cv2.rectangle(display, (x, y), (x + size - 1, y + size - 1), (0, 255, 0), 10)

        # display
        rgb = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)
        height, width, _ = rgb.shape
        image = QImage(rgb.data, width, height, rgb.strides[0], QImage.Format.Format_RGB888)
        self.preview.setPixmap(QPixmap.fromImage(image).scaled(
            self.preview.size(), Qt.AspectRatioMode.KeepAspectRatio
        ))

        if self.is_recording and time.monotonic() - self.last_capture >= CAPTURE_INTERVAL:
            self.save_photo(self.label)
            self.last_capture = time.monotonic()

    def hand_area(self):
        height, width = self.frame.shape[:2]
        size = min(height, width) * 3 // 5
        return width - size - 16, (height - size) // 2, size, size
    
    def save_photo(self, label):
        try:
            folder = DATA_DIR / str(label)
            folder.mkdir(parents=True, exist_ok=True)
            filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".jpg"

            x, y, width, height = self.hand_area()
            image = self.frame[y:y + height, x:x + width]
            cv2.imwrite(DATA_DIR / str(label) / filename, image)

        except (OSError, cv2.error) as error:
            self.is_recording = False
            print(f"Save Image ERROR：{error}")
            return
        
        self.save_frame_count += 1
        self.count_label.setText(f"{self.save_frame_count} frames have been saved.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())