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
    exists = db.query(Appointment).join(Appointment.patient).filter(
        Appointment.patient_id == payload.patient_id).first()
    # 여기서는 단순히 patient가 있는지만 확인하고 넘어가도 좋습니다.
    # 하지만 foreign key 제약이 있기 때문에 DB 삽입 시 에러가 터지면 400으로 변환해도 됩니다.

    # 2) 새 Appointment 객체 생성
    new_appt = Appointment(
        patient_id=payload.patient_id,
        appointment_day=payload.appointment_day or datetime.utcnow(),
        created_at=datetime.utcnow()
    )
    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)

    return new_appt
