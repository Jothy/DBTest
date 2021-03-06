import os
import sys
import io
import numpy as np
import sqlite3

from sqlalchemy import Column,Integer,Float,String,Binary,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



print("Showing differences...")

Base=declarative_base()


class Patient(Base):
    __tablename__='Patient'
    ID =Column(Integer,primary_key=True)
    Name=Column(String(50),nullable=False)

class Beam(Base):
    __tablename__='Beam'
    ID=Column(Integer,primary_key=True)
    Name=Column(String(15),nullable=True)
    Angle=Column(Float,nullable=True)
    PixelsLessThanOnePercent=Column(Float,nullable=False)
    PixelsLessThanThreePercent=Column(Float,nullable=False)
    PlannedFluence=Column(Binary,nullable=False)
    DeliveredFluence=Column(Binary,nullable=False)
    PatientAttached=relationship(Patient)
    PatientID=Column(Integer,ForeignKey('Patient.ID'))

def NumpyToSQLiteArray(nparray):
    out = io.BytesIO()
    np.save(out, nparray)
    out.seek(0)
    return sqlite3.Binary(out.read())

def SQLiteToNumpyArray(SQLiteArray):
    out = io.BytesIO(SQLiteArray)
    out.seek(0)
    return np.load(out)


def CreateEngine():
    engine=create_engine('sqlite:///FluDo.db')
    Base.metadata.create_all(engine)

#CreateEngine()

engine=create_engine('sqlite:///FluDo.db')
Base.metadata.bind=engine

DBSession=sessionmaker(bind=engine)
session=DBSession()

# NewPt=Patient(ID=123,Name='TestPat')
# session.add(NewPt)
# session.commit()

# Flu=np.arange(12).reshape(2,6)

# NewBeam=Beam(ID=2,Name='PA',Angle=0.0,PixelsLessThanOnePercent=97.0,PixelsLessThanThreePercent=98.5,PlannedFluence=Flu,DeliveredFluence=Flu,PatientID=123)
# session.add(NewBeam)
# session.commit()

p1=session.query(Patient).first()
print(p1.ID)
print(p1.Name)
print('------------')
b1=session.query(Beam).all()[1]
print(np.size(b1))

print(b1.ID)
print(b1.Name)
print(b1.Angle)
print(b1.PixelsLessThanOnePercent)
print(b1.PixelsLessThanThreePercent)















