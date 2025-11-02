"""
Unit tests for the Diagnostic System.
"""

import pytest
from datetime import datetime
from src.autonomous_vehicle.diagnostics import (
    DiagnosticSystem,
    DiagnosticLevel,
    DiagnosticReport,
)


@pytest.fixture
def diagnostic_config():
    """Diagnostic system configuration fixture."""
    return {
        "enabled": True,
        "check_interval_s": 1.0,
        "fault_tolerance": "high",
    }


@pytest.fixture
def diagnostic_system(diagnostic_config):
    """Diagnostic system fixture."""
    return DiagnosticSystem(diagnostic_config)


def test_diagnostic_system_initialization(diagnostic_system):
    """Test diagnostic system initializes correctly."""
    assert diagnostic_system.enabled is True
    assert diagnostic_system.check_interval == 1.0
    assert len(diagnostic_system.reports) == 0


def test_check_sensor_health_no_issues(diagnostic_system):
    """Test sensor health check with no issues."""
    sensor_data = {
        "lidar": {"status": "ok", "timestamp": datetime.now()},
        "camera_0": {"status": "ok", "timestamp": datetime.now()},
    }
    
    report = diagnostic_system.check_sensor_health(sensor_data)
    
    assert report.level == DiagnosticLevel.INFO
    assert "normally" in report.message.lower()


def test_check_sensor_health_with_error(diagnostic_system):
    """Test sensor health check with errors."""
    sensor_data = {
        "lidar": {"status": "error", "timestamp": datetime.now()},
    }
    
    report = diagnostic_system.check_sensor_health(sensor_data)
    
    assert report.level == DiagnosticLevel.WARNING
    assert "issues" in report.message.lower()


def test_check_sensor_health_no_data(diagnostic_system):
    """Test sensor health check with missing data."""
    sensor_data = {
        "lidar": None,
    }
    
    report = diagnostic_system.check_sensor_health(sensor_data)
    
    assert report.level == DiagnosticLevel.WARNING
    assert "no data" in report.message.lower()


def test_check_can_bus_connected(diagnostic_system):
    """Test CAN bus check when connected."""
    can_status = {
        "connected": True,
        "error_count": 0,
    }
    
    report = diagnostic_system.check_can_bus(can_status)
    
    assert report.level == DiagnosticLevel.INFO
    assert "normally" in report.message.lower()


def test_check_can_bus_disconnected(diagnostic_system):
    """Test CAN bus check when disconnected."""
    can_status = {
        "connected": False,
    }
    
    report = diagnostic_system.check_can_bus(can_status)
    
    assert report.level == DiagnosticLevel.ERROR
    assert "disconnected" in report.message.lower()


def test_check_control_system_ok(diagnostic_system):
    """Test control system check when OK."""
    control_status = {
        "steering_responsive": True,
        "brakes_responsive": True,
        "actuator_errors": 0,
    }
    
    report = diagnostic_system.check_control_system(control_status)
    
    assert report.level == DiagnosticLevel.INFO
    assert "normally" in report.message.lower()


def test_check_control_system_critical(diagnostic_system):
    """Test control system check with critical issues."""
    control_status = {
        "steering_responsive": False,
        "brakes_responsive": True,
        "actuator_errors": 0,
    }
    
    report = diagnostic_system.check_control_system(control_status)
    
    assert report.level == DiagnosticLevel.CRITICAL
    assert "steering" in report.message.lower()


def test_run_full_diagnostics(diagnostic_system):
    """Test full diagnostic run."""
    system_state = {
        "sensors": {
            "lidar": {"status": "ok", "timestamp": datetime.now()},
        },
        "can_bus": {
            "connected": True,
            "error_count": 0,
        },
        "control": {
            "steering_responsive": True,
            "brakes_responsive": True,
            "actuator_errors": 0,
        },
    }
    
    reports = diagnostic_system.run_full_diagnostics(system_state)
    
    assert len(reports) == 3
    assert all(isinstance(r, DiagnosticReport) for r in reports)


def test_get_critical_issues(diagnostic_system):
    """Test getting critical issues."""
    # Add some reports
    diagnostic_system.reports.append(
        DiagnosticReport(
            timestamp=datetime.now(),
            component="test",
            level=DiagnosticLevel.INFO,
            message="Info message",
        )
    )
    diagnostic_system.reports.append(
        DiagnosticReport(
            timestamp=datetime.now(),
            component="test",
            level=DiagnosticLevel.CRITICAL,
            message="Critical message",
        )
    )
    
    critical = diagnostic_system.get_critical_issues()
    
    assert len(critical) == 1
    assert critical[0].level == DiagnosticLevel.CRITICAL


def test_get_system_health_summary_healthy(diagnostic_system):
    """Test system health summary when healthy."""
    diagnostic_system.reports.append(
        DiagnosticReport(
            timestamp=datetime.now(),
            component="test",
            level=DiagnosticLevel.INFO,
            message="All good",
        )
    )
    
    summary = diagnostic_system.get_system_health_summary()
    
    assert summary["status"] == "healthy"
    assert summary["critical_count"] == 0


def test_get_system_health_summary_critical(diagnostic_system):
    """Test system health summary with critical issues."""
    diagnostic_system.reports.append(
        DiagnosticReport(
            timestamp=datetime.now(),
            component="test",
            level=DiagnosticLevel.CRITICAL,
            message="Critical issue",
        )
    )
    
    summary = diagnostic_system.get_system_health_summary()
    
    assert summary["status"] == "critical"
    assert summary["critical_count"] == 1


def test_clear_reports(diagnostic_system):
    """Test clearing diagnostic reports."""
    diagnostic_system.reports.append(
        DiagnosticReport(
            timestamp=datetime.now(),
            component="test",
            level=DiagnosticLevel.INFO,
            message="Test",
        )
    )
    
    assert len(diagnostic_system.reports) > 0
    
    diagnostic_system.clear_reports()
    
    assert len(diagnostic_system.reports) == 0
