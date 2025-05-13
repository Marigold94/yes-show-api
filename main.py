from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel

# === DB 설정 ===
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# === DB 모델 정의 ===
class PatientSurvey(Base):
    __tablename__ = "patient_survey"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    symptoms = Column(Text)
    diagnosis = Column(Text)
    treatment = Column(Text)
    precautions = Column(Text)
    patient_feedback = Column(Text)

# 테이블 생성
Base.metadata.create_all(bind=engine)

# === Pydantic 스키마 ===
class PatientSurveyCreate(BaseModel):
    name: str
    age: int
    symptoms: str
    diagnosis: str
    treatment: str
    precautions: str
    patient_feedback: str

class PatientSurveyOut(PatientSurveyCreate):
    id: int

    class Config:
        # v2+: from_attributes로 변경
        from_attributes = True

# === FastAPI 앱 초기화 ===
app = FastAPI()

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Task 1: 설문조사 API (POST) ===
@app.post("/survey", response_model=PatientSurveyOut)
def create_survey(data: PatientSurveyCreate, db: Session = Depends(get_db)):
    survey = PatientSurvey(**data.dict())
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return survey

# === Task 2: 고객 정보 검색 API (GET) ===
@app.get("/customer", response_model=list[PatientSurveyOut])
def get_customer(name: str, db: Session = Depends(get_db)):
    results = db.query(PatientSurvey).filter(PatientSurvey.name == name).all()
    if not results:
        raise HTTPException(status_code=404, detail="고객 정보를 찾을 수 없습니다.")
    return results
