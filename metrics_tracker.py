"""
Metrics tracking for SupplySentinel
Tracks historical performance metrics across sessions
"""

import json
import os
from datetime import datetime
from typing import Dict, List

METRICS_FILE = "metrics_history.json"

class MetricsTracker:
    def __init__(self):
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict:
        """Load metrics from file"""
        if os.path.exists(METRICS_FILE):
            try:
                with open(METRICS_FILE, 'r') as f:
                    return json.load(f)
            except:
                return self._default_metrics()
        return self._default_metrics()
    
    def _default_metrics(self) -> Dict:
        """Default metrics structure"""
        return {
            "total_scans": 0,
            "total_critical_alerts": 0,
            "total_risk_scores": [],
            "last_scan_timestamp": None,
            "scan_history": []
        }
    
    def _save_metrics(self):
        """Save metrics to file"""
        with open(METRICS_FILE, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def record_scan(self, suppliers_count: int, critical_count: int, risk_scores: List[float]):
        """Record a completed scan"""
        self.metrics["total_scans"] += suppliers_count
        self.metrics["total_critical_alerts"] += critical_count
        self.metrics["total_risk_scores"].extend(risk_scores)
        self.metrics["last_scan_timestamp"] = datetime.now().isoformat()
        
        # Add to scan history (keep last 100 scans)
        self.metrics["scan_history"].append({
            "timestamp": self.metrics["last_scan_timestamp"],
            "suppliers": suppliers_count,
            "critical": critical_count,
            "avg_risk": sum(risk_scores) / len(risk_scores) if risk_scores else 0
        })
        
        # Keep only last 100 scans
        if len(self.metrics["scan_history"]) > 100:
            self.metrics["scan_history"] = self.metrics["scan_history"][-100:]
        
        self._save_metrics()
    
    def get_total_scans(self) -> int:
        """Get total number of scans performed"""
        return self.metrics["total_scans"]
    
    def get_total_critical_alerts(self) -> int:
        """Get total critical alerts sent"""
        return self.metrics["total_critical_alerts"]
    
    def get_avg_risk_score(self) -> float:
        """Get average risk score across all scans"""
        scores = self.metrics["total_risk_scores"]
        if not scores:
            return 0.0
        return sum(scores) / len(scores)
    
    def get_last_scan_timestamp(self) -> str:
        """Get timestamp of last scan"""
        return self.metrics["last_scan_timestamp"]
    
    def get_recent_scans(self, limit: int = 10) -> List[Dict]:
        """Get recent scan history"""
        return self.metrics["scan_history"][-limit:]
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics = self._default_metrics()
        self._save_metrics()
