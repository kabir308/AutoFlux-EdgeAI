"""
Diagnostic System for Autonomous Vehicle

Monitors vehicle health, sensor status, and system integrity.
"""

import logging
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


class DiagnosticLevel(Enum):
    """Diagnostic severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class DiagnosticReport:
    """Diagnostic report data structure"""
    timestamp: datetime
    component: str
    level: DiagnosticLevel
    message: str
    code: Optional[str] = None
    data: Optional[Dict] = None


class DiagnosticSystem:
    """
    Main diagnostic system for autonomous vehicle monitoring.
    
    Responsible for:
    - Sensor health monitoring
    - System integrity checks
    - Error detection and reporting
    - Fault tolerance management
    """
    
    def __init__(self, config: Dict):
        """
        Initialize diagnostic system.
        
        Args:
            config: Diagnostic configuration dictionary
        """
        self.config = config
        self.enabled = config.get("enabled", True)
        self.check_interval = config.get("check_interval_s", 1.0)
        self.reports: List[DiagnosticReport] = []
        self.component_status: Dict[str, bool] = {}
        
        logger.info("Diagnostic system initialized")
    
    def check_sensor_health(self, sensor_data: Dict) -> DiagnosticReport:
        """
        Check health of sensor systems.
        
        Args:
            sensor_data: Dictionary containing sensor readings
            
        Returns:
            DiagnosticReport with sensor health status
        """
        issues = []
        
        for sensor_name, data in sensor_data.items():
            if data is None:
                issues.append(f"{sensor_name}: No data received")
            elif isinstance(data, dict):
                if data.get("status") == "error":
                    issues.append(f"{sensor_name}: Error state")
                elif data.get("timestamp"):
                    # Check for stale data
                    age = (datetime.now() - data["timestamp"]).total_seconds()
                    if age > 5.0:
                        issues.append(f"{sensor_name}: Stale data ({age:.1f}s)")
        
        if issues:
            level = DiagnosticLevel.WARNING
            message = f"Sensor issues detected: {'; '.join(issues)}"
        else:
            level = DiagnosticLevel.INFO
            message = "All sensors operating normally"
        
        report = DiagnosticReport(
            timestamp=datetime.now(),
            component="sensors",
            level=level,
            message=message,
            data={"issues": issues}
        )
        
        self.reports.append(report)
        return report
    
    def check_can_bus(self, can_status: Dict) -> DiagnosticReport:
        """
        Check CAN bus communication status.
        
        Args:
            can_status: CAN bus status information
            
        Returns:
            DiagnosticReport with CAN bus health
        """
        if not can_status.get("connected"):
            level = DiagnosticLevel.ERROR
            message = "CAN bus disconnected"
        elif can_status.get("error_count", 0) > 10:
            level = DiagnosticLevel.WARNING
            message = f"CAN bus errors: {can_status['error_count']}"
        else:
            level = DiagnosticLevel.INFO
            message = "CAN bus operating normally"
        
        report = DiagnosticReport(
            timestamp=datetime.now(),
            component="can_bus",
            level=level,
            message=message,
            data=can_status
        )
        
        self.reports.append(report)
        return report
    
    def check_control_system(self, control_status: Dict) -> DiagnosticReport:
        """
        Check vehicle control system status.
        
        Args:
            control_status: Control system status information
            
        Returns:
            DiagnosticReport with control system health
        """
        issues = []
        
        if not control_status.get("steering_responsive"):
            issues.append("Steering not responsive")
        
        if not control_status.get("brakes_responsive"):
            issues.append("Brakes not responsive")
        
        if control_status.get("actuator_errors", 0) > 0:
            issues.append(f"Actuator errors: {control_status['actuator_errors']}")
        
        if issues:
            level = DiagnosticLevel.CRITICAL
            message = f"Control system issues: {'; '.join(issues)}"
        else:
            level = DiagnosticLevel.INFO
            message = "Control system operating normally"
        
        report = DiagnosticReport(
            timestamp=datetime.now(),
            component="control",
            level=level,
            message=message,
            data={"issues": issues}
        )
        
        self.reports.append(report)
        return report
    
    def run_full_diagnostics(self, system_state: Dict) -> List[DiagnosticReport]:
        """
        Run complete diagnostic check on all systems.
        
        Args:
            system_state: Complete system state dictionary
            
        Returns:
            List of diagnostic reports
        """
        if not self.enabled:
            return []
        
        reports = []
        
        # Check sensors
        if "sensors" in system_state:
            reports.append(self.check_sensor_health(system_state["sensors"]))
        
        # Check CAN bus
        if "can_bus" in system_state:
            reports.append(self.check_can_bus(system_state["can_bus"]))
        
        # Check control system
        if "control" in system_state:
            reports.append(self.check_control_system(system_state["control"]))
        
        return reports
    
    def get_critical_issues(self) -> List[DiagnosticReport]:
        """
        Get all critical diagnostic issues.
        
        Returns:
            List of critical diagnostic reports
        """
        return [
            report for report in self.reports
            if report.level in [DiagnosticLevel.ERROR, DiagnosticLevel.CRITICAL]
        ]
    
    def clear_reports(self):
        """Clear diagnostic report history."""
        self.reports.clear()
        logger.debug("Diagnostic reports cleared")
    
    def get_system_health_summary(self) -> Dict:
        """
        Get overall system health summary.
        
        Returns:
            Dictionary with health summary
        """
        if not self.reports:
            return {"status": "unknown", "message": "No diagnostic data"}
        
        recent_reports = self.reports[-10:]  # Last 10 reports
        
        critical_count = sum(1 for r in recent_reports if r.level == DiagnosticLevel.CRITICAL)
        error_count = sum(1 for r in recent_reports if r.level == DiagnosticLevel.ERROR)
        warning_count = sum(1 for r in recent_reports if r.level == DiagnosticLevel.WARNING)
        
        if critical_count > 0:
            status = "critical"
            message = f"{critical_count} critical issue(s) detected"
        elif error_count > 0:
            status = "error"
            message = f"{error_count} error(s) detected"
        elif warning_count > 0:
            status = "warning"
            message = f"{warning_count} warning(s) detected"
        else:
            status = "healthy"
            message = "All systems operational"
        
        return {
            "status": status,
            "message": message,
            "critical_count": critical_count,
            "error_count": error_count,
            "warning_count": warning_count,
        }
