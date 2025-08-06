import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="EHB EDR Service",
    description="Exam Decision Registration Service",
    version="1.0.0"
)


class ExamRequest(BaseModel):
    exam_name: str
    candidate_id: str
    exam_type: str
    details: dict


class ExamResponse(BaseModel):
    exam_id: str
    status: str
    scheduled_at: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EDR",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "capabilities": [
            "Exam Registration",
            "Skill Testing",
            "Certification"
        ]
    }


@app.get("/")
def root():
    return {
        "message": "EHB EDR Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "exam": "/exam",
            "stats": "/stats"
        }
    }


@app.post("/exam")
def register_exam(exam: ExamRequest):
    """Register for an exam"""
    exam_id = f"EDR_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    return ExamResponse(
        exam_id=exam_id,
        status="scheduled",
        scheduled_at=datetime.datetime.now().isoformat()
    )


@app.get("/exam/{exam_id}")
def get_exam(exam_id: str):
    """Get exam details"""
    return {
        "exam_id": exam_id,
        "name": "Sample Exam",
        "type": "Technical",
        "status": "scheduled",
        "scheduled_at": datetime.datetime.now().isoformat()
    }


@app.get("/stats")
def get_stats():
    """Get EDR service statistics"""
    return {
        "total_exams": 320,
        "completed_exams": 280,
        "scheduled_exams": 25,
        "failed_exams": 15,
        "success_rate": 87.5
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4002)
