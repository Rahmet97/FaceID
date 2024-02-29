import numpy as np
import json

from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, TIMESTAMP
from database import Base

metadata = MetaData()


class User(Base):
    __tablename__ = 'users'
    metadata=metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    face_encodings = Column(String)

    def __init__(self, name, face_encodings):
        self.name = name
        self.face_encodings = json.dumps(face_encodings.tolist())

    def get_array(self):
        return np.array(json.loads(self.face_encodings))


class UserIOTime(Base):
    __tablename__ = 'users_io_times'
    metadata=metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('users.id'))
    enter_time = Column(TIMESTAMP)
    exit_time = Column(TIMESTAMP)
