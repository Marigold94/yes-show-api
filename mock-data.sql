DROP TABLE IF EXISTS patient_survey;

CREATE TABLE patient_survey (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    symptoms TEXT,
    diagnosis TEXT,
    treatment TEXT,
    precautions TEXT,
    patient_feedback TEXT
);

INSERT INTO patient_survey (name, age, symptoms, diagnosis, treatment, precautions, patient_feedback) VALUES
('홍길동', 45, '목과 오른쪽 어깨의 뻐근함과 통증, 컴퓨터 사용 시 증상 악화', '근막통증증후군 가능성, 경추 염좌 또는 긴장도 의심', '근육이완제 및 소염진통제 처방, 도수치료 시작 권고', '약물 복용 시 주의사항 안내 및 정확한 운동 지도 필요', '환자가 처방 및 치료 방향에 동의함'),
('김영희', 30, '오른쪽 손목 통증, 마우스 사용 시 악화', '손목 터널 증후군 의심', '손목 보조기 착용, 스트레칭 교육', '장시간 사용 피하기, 틈틈이 스트레칭 권장', '보조기 착용에 긍정적인 반응'),
('박철수', 52, '왼쪽 무릎 통증, 계단 오를 때 심화', '슬개골 연골 연화증 가능성', '냉찜질 및 물리치료 권장', '무리한 운동 삼가, 체중 조절 필요', '운동 제한에 이해와 동의함');
