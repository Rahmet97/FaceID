import sys
import cv2
import sqlite3
import os
from datetime import datetime
from PyQt6.uic import loadUi
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("./FaceRec.ui", self)
        self.setWindowTitle("IP Camera and Face Recognition")
        self.db_connection = sqlite3.connect('faces.db') # DB nomi va manzili
        self.create_table()
        self.image_save_folder = 'ImagesAttendance'
        os.makedirs(self.image_save_folder, exist_ok=True)

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS faces
                          (id INTEGER PRIMARY KEY,
                           name TEXT,
                           image BLOB,
                           date_time TEXT)''')
        self.db_connection.commit()

    def start_video_stream(self):
        self.capture = cv2.VideoCapture(0) # or IP camera url
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // 30)  # 30 FPS

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            # Yuzni aniqlash
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face_image = frame[y:y+h, x:x+w]
                face_image = cv2.resize(face_image, (100, 100))  # Resize qiling
                face_blob = cv2.imencode('.jpg', face_image)[1].tobytes()  # Yuzning blob sifatida kodlangan ma'lumotlari

                # Yuzni aniqlash va bazaga saqlash
                name = self.detect_and_save_face(face_image)

                # Yuzni tortburchak qilib ajratib chiqarish
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Tasvirda yuzlarni ko'rsatish
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.imgLabel.setPixmap(pixmap)
            self.imgLabel.setScaledContents(True)

            # Joriy sana va vaqt
            current_date = datetime.now()
            self.DateLabel.setText(str(current_date.strftime('%d.%b.%Y')))
            self.TimeLabel.setText(str(current_date.strftime('%H:%M:%S')))

    def detect_and_save_face(self, face_image):
        # Tanilgan yuzni bazaga qo'shish
        cursor = self.db_connection.cursor()
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''INSERT INTO faces (name, image, date_time)
                          VALUES (?, ?, ?)''', ('User', face_image, current_date_time))
        self.db_connection.commit()

        # Yuzni saqlash
        image_path = os.path.join(self.image_save_folder, f'{current_date_time}.jpg')
        cv2.imwrite(image_path, face_image)

        return 'User'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.start_video_stream()
    sys.exit(app.exec())
