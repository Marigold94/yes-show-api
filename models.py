from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)  # 생년월일 (나이 계산용)
    gender = Column(String(10), nullable=False)
    national_id = Column(String(20), unique=True)
    phone_number = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    emergency_contact_name = Column(String(100))
    emergency_contact_phone = Column(String(20))
    blood_type = Column(String(3))

    # 캐싱 컬럼 (뷰/트리거 등으로 갱신하거나, 필요시만 둬도 됨)
    first_visit_date = Column(Date)
    last_visit_date = Column(Date)
    total_visit_count = Column(Integer)
    last_prescription_id = Column(Integer, ForeignKey("prescription.id"))

    # 처방/방문기록 연결
    prescriptions = relationship(
        "Prescription",
        back_populates="patient",
        foreign_keys=lambda: [Prescription.patient_id]
    )
    visits = relationship("Visit", back_populates="patient")
    last_prescription = relationship(
        "Prescription",
        foreign_keys=[last_prescription_id],
    )
    appointments = relationship("Appointment", back_populates="patient")


# Prescription, Visit 테이블도 아래와 같이 필요

class Prescription(Base):
    __tablename__ = "prescription"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    prescribed_date = Column(Date, nullable=False)
    medication_name = Column(String(100), nullable=False)
    dosage = Column(String(50))
    duration_days = Column(Integer)
    notes = Column(Text)

    patient = relationship(
        "Patient",
        back_populates="prescriptions",
        foreign_keys=[patient_id]
    )


class Visit(Base):
    __tablename__ = "visit"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    visit_date = Column(Date, nullable=False)
    doctor_name = Column(String(100))
    reason = Column(Text)

    patient = relationship("Patient", back_populates="visits")


class Appointment(Base):
    __tablename__ = "appointment"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    name = Column(String(100), nullable=False, index=True)  # 추가된 name 필드
    memo = Column(Text, nullable=True)
    script = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    no_show = Column(Boolean, default=False)
    appointment_day = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    patient = relationship("Patient", back_populates="appointments")
