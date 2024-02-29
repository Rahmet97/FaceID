import sys
import cv2
from datetime import datetime
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QDialog, QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("./FaceRec.ui", self)
        self.setWindowTitle("IP Camera and Face Recognition")


    def start_video_stream(self):
        self.capture = cv2.VideoCapture(0) # or IP camera url
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // 30)  # 30 FPS

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.imgLabel.setPixmap(pixmap)
            self.imgLabel.setScaledContents(True)

            current_date = datetime.now()
            self.DateLabel.setText(str(current_date.strftime('%d.%b.%Y')))
            self.TimeLabel.setText(str(current_date.strftime('%H:%M:%S')))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.start_video_stream()
    sys.exit(app.exec())
