from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import PatientSurvey
from schemas import PatientSurveyCreate, PatientSurveyOut

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
@app.post("/survey", response_model=PatientSurveyOut)
def create_survey(data: PatientSurveyCreate, db: Session = Depends(get_db)):
    survey = PatientSurvey(**data.dict())
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return survey


# 고객 이름 검색 API
@app.get("/customer", response_model=list[PatientSurveyOut])
def get_customer(name: str, db: Session = Depends(get_db)):
    results = db.query(PatientSurvey).filter(PatientSurvey.name == name).all()
    if not results:
        raise HTTPException(status_code=404, detail="고객 정보를 찾을 수 없습니다.")
    return results
