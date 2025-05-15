from sqlalchemy import Column, Integer, String, Text
from database import Base


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
