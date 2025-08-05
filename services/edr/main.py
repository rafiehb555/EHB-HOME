from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="EDR - Exam Decision Registration",
    description="EHB Exam Decision Registration API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ExamRegistration(BaseModel):
    user_id: int
    exam_name: str
    exam_type: str
    exam_date: str
    exam_center: str
    registration_fee: float

class ExamResult(BaseModel):
    user_id: int
    exam_id: str
    score: float
    grade: str
    status: str
    result_date: datetime

class DecisionRequest(BaseModel):
    user_id: int
    decision_type: str
    decision_data: dict
    priority: str

# Mock data
exam_registrations = {
    1: [
        {
            "exam_id": "EDR_001",
            "exam_name": "Professional Certification",
            "exam_type": "certification",
            "exam_date": "2024-03-15",
            "exam_center": "Tech Center A",
            "registration_fee": 150.00,
            "status": "registered"
        }
    ],
    2: [
        {
            "exam_id": "EDR_002",
            "exam_name": "Skill Assessment",
            "exam_type": "assessment",
            "exam_date": "2024-03-20",
            "exam_center": "Assessment Center B",
            "registration_fee": 75.00,
            "status": "pending"
        }
    ]
}

exam_results = {
    "EDR_001": {
        "user_id": 1,
        "exam_id": "EDR_001",
        "score": 85.5,
        "grade": "B+",
        "status": "passed",
        "result_date": datetime.now()
    }
}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "EDR - Exam Decision Registration",
        "version": "1.0.0",
        "status": "running",
        "port": 4002
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "EDR",
        "timestamp": datetime.now()
    }

@app.get("/registrations/{user_id}")
async def get_user_registrations(user_id: int):
    """Get user's exam registrations"""
    if user_id not in exam_registrations:
        return {"user_id": user_id, "registrations": []}

    return {
        "user_id": user_id,
        "registrations": exam_registrations[user_id],
        "total_registrations": len(exam_registrations[user_id])
    }

@app.post("/register-exam")
async def register_exam(registration: ExamRegistration):
    """Register for an exam"""
    exam_id = f"EDR_{registration.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    new_registration = {
        "exam_id": exam_id,
        "exam_name": registration.exam_name,
        "exam_type": registration.exam_type,
        "exam_date": registration.exam_date,
        "exam_center": registration.exam_center,
        "registration_fee": registration.registration_fee,
        "status": "registered"
    }

    if registration.user_id not in exam_registrations:
        exam_registrations[registration.user_id] = []

    exam_registrations[registration.user_id].append(new_registration)

    return {
        "message": "Exam registration successful",
        "exam_id": exam_id,
        "registration": new_registration
    }

@app.get("/results/{user_id}")
async def get_user_results(user_id: int):
    """Get user's exam results"""
    user_results = [
        result for result in exam_results.values()
        if result["user_id"] == user_id
    ]

    return {
        "user_id": user_id,
        "results": user_results,
        "total_results": len(user_results)
    }

@app.get("/result/{exam_id}")
async def get_exam_result(exam_id: str):
    """Get specific exam result"""
    if exam_id not in exam_results:
        raise HTTPException(status_code=404, detail="Exam result not found")

    return exam_results[exam_id]

@app.post("/submit-decision")
async def submit_decision(decision: DecisionRequest):
    """Submit a decision request"""
    decision_id = f"EDR_DEC_{decision.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Mock decision processing
    if decision.decision_type == "exam_approval":
        status = "approved"
        message = "Exam approval decision submitted successfully"
    elif decision.decision_type == "result_review":
        status = "pending"
        message = "Result review decision submitted for processing"
    else:
        status = "under_review"
        message = "Decision submitted for review"

    return {
        "decision_id": decision_id,
        "user_id": decision.user_id,
        "decision_type": decision.decision_type,
        "status": status,
        "message": message,
        "submitted_at": datetime.now()
    }

@app.get("/available-exams")
async def get_available_exams():
    """Get list of available exams"""
    return {
        "exams": [
            {
                "exam_name": "Professional Certification",
                "exam_type": "certification",
                "duration": "3 hours",
                "fee": 150.00,
                "next_date": "2024-03-15"
            },
            {
                "exam_name": "Skill Assessment",
                "exam_type": "assessment",
                "duration": "2 hours",
                "fee": 75.00,
                "next_date": "2024-03-20"
            },
            {
                "exam_name": "Technical Evaluation",
                "exam_type": "evaluation",
                "duration": "4 hours",
                "fee": 200.00,
                "next_date": "2024-03-25"
            }
        ]
    }

@app.get("/exam-centers")
async def get_exam_centers():
    """Get available exam centers"""
    return {
        "centers": [
            {
                "center_id": "TC_A",
                "name": "Tech Center A",
                "address": "123 Tech Street, Tech City",
                "capacity": 50,
                "available_slots": 15
            },
            {
                "center_id": "AC_B",
                "name": "Assessment Center B",
                "address": "456 Assessment Ave, Test City",
                "capacity": 30,
                "available_slots": 8
            },
            {
                "center_id": "EC_C",
                "name": "Evaluation Center C",
                "address": "789 Evaluation Road, Exam City",
                "capacity": 40,
                "available_slots": 12
            }
        ]
    }

@app.get("/exam-schedule/{user_id}")
async def get_exam_schedule(user_id: int):
    """Get user's exam schedule"""
    if user_id not in exam_registrations:
        return {"user_id": user_id, "schedule": []}

    schedule = []
    for registration in exam_registrations[user_id]:
        if registration["status"] in ["registered", "confirmed"]:
            schedule.append({
                "exam_id": registration["exam_id"],
                "exam_name": registration["exam_name"],
                "exam_date": registration["exam_date"],
                "exam_center": registration["exam_center"],
                "status": registration["status"]
            })

    return {
        "user_id": user_id,
        "schedule": schedule,
        "total_exams": len(schedule)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4002, reload=True)
