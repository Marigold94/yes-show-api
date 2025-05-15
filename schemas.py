from pydantic import BaseModel


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
        from_attributes = True
