from typing import List, Dict, Any
import pandas as pd

class AnalyticsService:
    """
    Deterministic engine for anomaly detection.
    No AI is used here - only pure mathematical logic.
    """
    def __init__(self, threshold_pct: float = 5.0):
        self.threshold_pct = threshold_pct

    def _get_val(self, m: Any, key: str) -> Any:
        if isinstance(m, dict):
            return m.get(key, 0)
        return getattr(m, key, 0)

    def detect_anomalies(self, metrics: List[Any]) -> List[Dict[str, Any]]:
        """
        Analyze metrics and flag anomalies based on deterministic thresholds.
        """
        anomalies = []
        for m in metrics:
            # Calculate percentage change
            prev = self._get_val(m, 'previous_value')
            curr = self._get_val(m, 'current_value')

            if prev == 0:
                delta_pct = 100.0 if curr > 0 else 0.0
            else:
                delta_pct = ((curr - prev) / prev) * 100

            # Flag as anomaly if it exceeds threshold
            is_anomaly = abs(delta_pct) >= self.threshold_pct

            if is_anomaly:
                anomalies.append({
                    "metric_id": self._get_val(m, 'metric_id'),
                    "metric_name": self._get_val(m, 'metric_name'),
                    "delta_pct": round(delta_pct, 2),
                    "severity": "CRITICAL" if abs(delta_pct) > 20 else "WARNING",
                    "status": "Detected"
                })

        return anomalies

    def calculate_segment_contribution(self, current_data_path: str, prev_data_path: str, target_col: str):
        """
        Identifies which segment (e.g. 'Credit Card') contributed most to the increase.
        """
        curr_df = pd.read_csv(current_data_path)
        prev_df = pd.read_csv(prev_data_path)
        
        # Group by risk category and sum exposure
        curr_sum = curr_df.groupby('risk_category')[target_col].sum()
        prev_sum = prev_df.groupby('risk_category')[target_col].sum()
        
        diff = curr_sum - prev_sum
        top_contributor = diff.idxmax()
        contribution_amount = diff.max()
        
        return {
            "top_contributor": top_contributor,
            "amount": contribution_amount,
            "contribution_pct": (contribution_amount / curr_sum.sum()) * 100
        }
