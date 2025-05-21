from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Patient
from schemas import PatientInfoCreate, PatientInfoOut

# DB 테이블 자동 생성 (이미 있으면 아무 일도 안 함)
from database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
