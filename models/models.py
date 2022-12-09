from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import datetime
from database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    name = Column(String)
    password = Column(String)

class Motor(Base):
    __tablename__ = 'motor_mahasiswa'
    
    id = Column(Integer, primary_key=True, index=True)
    id_tempat_parkir = Column(Integer, ForeignKey('tempat_parkir_mahasiswa.id'))
    plat_motor = Column(String)
    jam_masuk = Column(DateTime, default=datetime.datetime.now())
    jam_keluar = Column(DateTime)

    tempat_parkir = relationship("TempatParkir", back_populates="motor_parkir")

    def update(self, jam_keluar=None):
        if jam_keluar:
            self.jam_keluar = jam_keluar

class TempatParkir(Base):
    __tablename__ = 'tempat_parkir_mahasiswa'

    id = Column(Integer, primary_key=True)
    tempat_parkir = Column(String)
    kuota = Column(Integer)

    motor_parkir = relationship("Motor", back_populates="tempat_parkir")