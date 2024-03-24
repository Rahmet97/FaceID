import os
import cv2
import face_recognition

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

from config import DB_HOST, DB_USER, DB_PORT, DB_NAME, DB_PASSWORD

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

Session = sessionmaker(bind=engine)
session = Session()

path = 'ImagesAttendance'
if not os.path.exists(path):
    os.mkdir(path)

attendance_list = os.listdir(path)

for cl in attendance_list:
    cur_img = cv2.imread(f'{path}/{cl}')
    img = cv2.cvtColor(cur_img, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(img)
    encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
    name = os.path.splitext(cl)[0]
    user = User(
        name=name,
        face_encodings=encodes_cur_frame
    )
    session.add(user)


session.commit()
session.close()