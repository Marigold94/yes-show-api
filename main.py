from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import engine, get_db
from models import Patient, Appointment
from schemas import (PatientInfoCreate, PatientInfoOut, AppointmentRead, AppointmentCreate, SummaryResponse,
                     ScriptResponse, MemoResponse, ScriptResponseList, MemoResponseList, SummaryResponseList)

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


# --- ID 기반 API (단일 결과) ---

# 1. Script 조회 API (ID 기반)
@app.get("/appointments/{appointment_id}/script", response_model=ScriptResponse, tags=["appointments"])
def get_appointment_script_by_id(patient_id: int, db: Session = Depends(get_db)):
    """
    특정 예약 ID의 script 필드를 반환합니다.
    """
    appointment = db.query(Appointment).filter(Appointment.patient_id == patient_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다.")

    return {"script": appointment.script}


# 2. Summary 조회 API (ID 기반)
@app.get("/appointments/{appointment_id}/summary", response_model=SummaryResponse, tags=["appointments"])
def get_appointment_summary_by_id(patient_id: int, db: Session = Depends(get_db)):
    """
    특정 예약 ID의 summary 필드를 반환합니다.
    """
    appointment = db.query(Appointment).filter(Appointment.patient_id == patient_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다.")

    return {"summary": appointment.summary}


# 3. Memo 조회 API (ID 기반)
@app.get("/appointments/{appointment_id}/memo", response_model=MemoResponse, tags=["appointments"])
def get_appointment_memo_by_id(patient_id: int, db: Session = Depends(get_db)):
    """
    특정 예약 ID의 memo 필드를 반환합니다.
    """
    appointment = db.query(Appointment).filter(Appointment.patient_id == patient_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다.")

    return {"memo": appointment.memo}


# --- 이름 기반 API (복수 결과) ---

# 4. 이름으로 예약 조회 API
@app.get("/appointments/by-name/{name}", response_model=list[AppointmentRead], tags=["appointments"])
def get_appointments_by_name(name: str, db: Session = Depends(get_db)):
    """
    예약자 이름으로 예약 목록을 조회합니다.
    """
    appointments = db.query(Appointment).filter(Appointment.name == name).all()
    if not appointments:
        raise HTTPException(status_code=404, detail=f"이름 '{name}'으로 예약을 찾을 수 없습니다.")

    return appointments


# 5. 이름으로 Script 조회 API
@app.get("/appointments/by-name/{name}/script", response_model=ScriptResponseList, tags=["appointments"])
def get_appointment_script_by_name(name: str, db: Session = Depends(get_db)):
    """
    예약자 이름으로 script 필드 목록을 반환합니다.
    """
    appointments = db.query(Appointment).filter(Appointment.name == name).all()
    if not appointments:
        raise HTTPException(status_code=404, detail=f"이름 '{name}'으로 예약을 찾을 수 없습니다.")

    scripts = [{"script": appointment.script} for appointment in appointments]
    return {"items": scripts}


# 6. 이름으로 Summary 조회 API
@app.get("/appointments/by-name/{name}/summary", response_model=SummaryResponseList, tags=["appointments"])
def get_appointment_summary_by_name(name: str, db: Session = Depends(get_db)):
    """
    예약자 이름으로 summary 필드 목록을 반환합니다.
    """
    appointments = db.query(Appointment).filter(Appointment.name == name).all()
    if not appointments:
        raise HTTPException(status_code=404, detail=f"이름 '{name}'으로 예약을 찾을 수 없습니다.")

    summaries = [{"summary": appointment.summary} for appointment in appointments]
    return {"items": summaries}


# 7. 이름으로 Memo 조회 API
@app.get("/appointments/by-name/{name}/memo", response_model=MemoResponseList, tags=["appointments"])
def get_appointment_memo_by_name(name: str, db: Session = Depends(get_db)):
    """
    예약자 이름으로 memo 필드 목록을 반환합니다.
    """
    appointments = db.query(Appointment).filter(Appointment.name == name).all()
    if not appointments:
        raise HTTPException(status_code=404, detail=f"이름 '{name}'으로 예약을 찾을 수 없습니다.")

    memos = [{"memo": appointment.memo} for appointment in appointments]
    return {"items": memos}
