import os
from typing import List, Dict, Any, Optional
from ..models.report import Report, ReportMetric

class FirestoreService:
    """
    Service to handle all Firestore interactions.
    Implements a Mock mode for local development without GCP credentials.
    """
    def __init__(self):
        self.mock_mode = os.getenv("ENVIRONMENT") == "development"
        if not self.mock_mode:
            import firebase_admin
            from firebase_admin import firestore

            FIREBASE_PROJECT_ID = os.getenv(
                "FIREBASE_PROJECT_ID",
                "regalis-ai-4f46e",
            )
            FIREBASE_APP_NAME = "regalis-auth"

            try:
                firebase_app = firebase_admin.get_app(FIREBASE_APP_NAME)
            except ValueError:
                firebase_app = firebase_admin.initialize_app(
                    options={"projectId": FIREBASE_PROJECT_ID},
                    name=FIREBASE_APP_NAME,
                )

            self.db = firestore.client(app=firebase_app)

        else:
            print("🛠️ FirestoreService running in MOCK mode")
            # Synthetic data for local dev
            self._mock_reports = {
                "rep_credit_risk_2026_09": {
                    "id": "rep_credit_risk_2026_09",
                    "name": "Credit Risk Exposure Report",
                    "period": "September 2026",
                    "status": "Anomaly Detected"
                }
            }
            self._mock_metrics = {
                "total_exposure": {
                    "metric_id": "total_exposure",
                    "metric_name": "Total Exposure",
                    "previous_value": 100000000,
                    "current_value": 117800000,
                    "delta_pct": 17.8,
                    "is_anomaly": True
                },
                "high_risk_count": {
                    "metric_id": "high_risk_count",
                    "metric_name": "High Risk Count",
                    "previous_value": 80000,
                    "current_value": 125000,
                    "delta_pct": 56.25,
                    "is_anomaly": True
                }
            }

    async def get_report(self, report_id: str) -> Optional[Report]:
        if self.mock_mode:
            data = self._mock_reports.get(report_id)
            return Report(**data) if data else None
        
        doc = self.db.collection('reports').document(report_id).get()
        if doc.exists:
            return Report(id=doc.id, **doc.to_dict())
        return None

    async def get_metrics_for_report(self, report_id: str) -> List[ReportMetric]:
        if self.mock_mode:
            return [ReportMetric(**m) for m in self._mock_metrics.values()]
        
        docs = self.db.collection('report_metrics').where('reportId', '==', report_id).stream()
        return [ReportMetric(metric_id=doc.id, **doc.to_dict()) for doc in docs]

    async def create_investigation(self, data: Dict[str, Any]) -> str:
        if self.mock_mode:
            inv_id = "inv_mock_123"
            print(f"🛠️ Mock creating investigation {inv_id}")
            return inv_id
        
        _, doc_ref = self.db.collection('investigations').add(data)
        return doc_ref.id
