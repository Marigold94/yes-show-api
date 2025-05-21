from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal, engine, get_db
from models import Patient, Appointment
from schemas import PatientInfoCreate, PatientInfoOut, AppointmentRead, AppointmentCreate

# DB 테이블 자동 생성 (이미 있으면 아무 일도 안 함)
from database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


# 설문조사 저장 API
@app.post("/write_patient_info", response_model=PatientInfoOut)
def create_survey(data: PatientInfoCreate, db: Session = Depends(get_db)):
    patient_info = Patient(**data.dict())
    db.add(patient_info)
    db.commit()
    db.refresh(patient_info)
    return patient_info


# 고객 이름 검색 API
@app.get("/get_patient_name", response_model=list[PatientInfoOut])
def get_patient_name(name: str, db: Session = Depends(get_db)):
    results = db.query(Patient).filter(Patient.name == name).all()
    if not results:
        raise HTTPException(status_code=404, detail="환자 정보를 찾을 수 없습니다.")
    return results


@app.post("/appointments", response_model=AppointmentRead)
def create_appointment(
        payload: AppointmentCreate,
        db: Session = Depends(get_db),
):
    # 1) patient_id 유효성 검사 (옵션)
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="등록되지 않은 환자입니다.")

    # 2) 새 Appointment 객체 생성
    new_appt = Appointment(
        patient_id=payload.patient_id,
        name=payload.name,  # 이름 설정
        memo=payload.memo,
        script=payload.script,
        summary=payload.summary,
        appointment_day=payload.appointment_day or datetime.utcnow(),
        created_at=datetime.utcnow()
    )
    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)

    return new_appt


@app.get("/appointments/by-name/{name}", response_model=list[AppointmentRead])
def get_appointments_by_name(name: str, db: Session = Depends(get_db)):
    """이름으로 예약 검색"""
    appointments = db.query(Appointment).filter(Appointment.name == name).all()
    if not appointments:
        raise HTTPException(status_code=404, detail="해당 이름의 예약을 찾을 수 없습니다.")
    return appointments


@app.get("/appointments/by-name", response_model=list[AppointmentRead])
def search_appointments_by_name(name: str, db: Session = Depends(get_db)):
    """이름 일부로 예약 검색 (부분 일치)"""
    # 이름에 검색어가 포함된 모든 예약 검색 (대소문자 구분 없음)
    appointments = db.query(Appointment).filter(
        Appointment.name.ilike(f"%{name}%")
    ).all()

    if not appointments:
        raise HTTPException(status_code=404, detail="검색 조건에 맞는 예약을 찾을 수 없습니다.")
    return appointments
