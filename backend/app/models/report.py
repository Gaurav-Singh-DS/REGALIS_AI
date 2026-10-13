from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ReportMetric(BaseModel):
    metric_id: str
    metric_name: str
    previous_value: float
    current_value: float
    delta_pct: float
    is_anomaly: bool

class Report(BaseModel):
    id: str
    name: str
    period: str
    status: str
    createdAt: Optional[datetime] = None
