from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .services.firestore_service import FirestoreService
from .models.report import Report, ReportMetric
from .agents.orchestrator import OrchestratorAgent
from .security.auth import get_current_user
from typing import List

app = FastAPI(title="REGREPORT AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://regalis-ai-4f46e.web.app",
        "https://regalis-ai-4f46e.firebaseapp.com",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


def get_db():
    return FirestoreService()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/api/reports/{report_id}", response_model=Report)
async def get_report(
    report_id: str,
    db: FirestoreService = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    report = await db.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.get("/api/reports/{report_id}/metrics", response_model=List[ReportMetric])
async def get_metrics(
    report_id: str,
    db: FirestoreService = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await db.get_metrics_for_report(report_id)

@app.post("/api/investigations/{report_id}")
async def start_investigation(
    report_id: str,
    db: FirestoreService = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # 1. Get metrics to feed the agents
    metrics = await db.get_metrics_for_report(report_id)

    # 2. Run the Orchestrator
    orchestrator = OrchestratorAgent()
    result = await orchestrator.investigate(report_id, metrics)

    # 3. Store investigation in DB
    inv_id = await db.create_investigation({
        "reportId": report_id,
        "result": result,
        "status": "Completed"
    })

    return {"investigationId": inv_id, **result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
