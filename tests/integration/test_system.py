"""
Integration tests for AutoFlux System.
"""

import pytest
import yaml
from pathlib import Path
from src.integration.system import AutoFluxSystem


@pytest.fixture
def test_config():
    """Test configuration fixture."""
    return {
        "autonomous_vehicle": {
            "sensors": {
                "lidar": {"enabled": True, "update_rate_hz": 10},
                "camera": {"enabled": True, "num_cameras": 2},
                "gps": {"enabled": True},
            },
            "control": {
                "mode": "assisted",
                "max_speed_mps": 20.0,
            },
            "diagnostics": {
                "enabled": True,
                "check_interval_s": 1.0,
            },
        },
        "neuroflux": {
            "models": {
                "object_detection": {
                    "model_name": "yolov8n",
                    "confidence_threshold": 0.5,
                    "input_size": [640, 640],
                },
            },
            "hardware": {
                "accelerator": "cpu",
                "precision": "fp32",
            },
        },
        "integration": {
            "system": {
                "update_rate_hz": 30,
            },
            "monitoring": {
                "log_level": "INFO",
            },
        },
    }


@pytest.fixture
def autoflux_system(test_config, tmp_path):
    """AutoFlux system fixture."""
    # Create temporary config file
    config_path = tmp_path / "test_config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(test_config, f)
    
    system = AutoFluxSystem(config_path=str(config_path))
    return system


def test_system_creation(autoflux_system):
    """Test system can be created."""
    assert autoflux_system is not None
    assert autoflux_system.running is False


def test_system_initialization(autoflux_system):
    """Test system initialization."""
    autoflux_system.initialize()
    
    assert autoflux_system.sensor_manager is not None
    assert autoflux_system.diagnostic_system is not None
    assert autoflux_system.vehicle_controller is not None
    assert autoflux_system.model_manager is not None
    assert autoflux_system.inference_engine is not None
    assert autoflux_system.orchestrator is not None


def test_system_start_stop(autoflux_system):
    """Test system start and stop."""
    autoflux_system.initialize()
    
    autoflux_system.start()
    assert autoflux_system.running is True
    
    autoflux_system.stop()
    assert autoflux_system.running is False


def test_system_status(autoflux_system):
    """Test getting system status."""
    autoflux_system.initialize()
    
    status = autoflux_system.get_system_status()
    
    assert "running" in status
    assert "sensors" in status
    assert "diagnostics" in status
    assert "control" in status
    assert "models" in status
    assert "inference" in status


def test_system_status_before_init(autoflux_system):
    """Test getting status before initialization."""
    status = autoflux_system.get_system_status()
    
    assert status["status"] == "not_initialized"


def test_emergency_stop(autoflux_system):
    """Test emergency stop functionality."""
    autoflux_system.initialize()
    autoflux_system.start()
    
    autoflux_system.emergency_stop()
    
    assert autoflux_system.vehicle_controller.emergency_stop is True


def test_get_version(autoflux_system):
    """Test getting system version."""
    version = autoflux_system.get_version()
    
    assert version == "1.0.0"


def test_system_repr(autoflux_system):
    """Test system string representation."""
    repr_str = repr(autoflux_system)
    
    assert "AutoFluxSystem" in repr_str
    assert "stopped" in repr_str


def test_system_with_default_config():
    """Test system with default configuration."""
    system = AutoFluxSystem(config_path="nonexistent.yaml")
    
    assert system.config is not None
    # Should fall back to defaults


def test_full_system_cycle(autoflux_system):
    """Test complete system processing cycle."""
    autoflux_system.initialize()
    autoflux_system.start()
    
    # Run one processing cycle
    if autoflux_system.orchestrator:
        autoflux_system.orchestrator.process_cycle()
        
        # Check that cycle was processed
        assert autoflux_system.orchestrator.cycle_count > 0
    
    autoflux_system.stop()


def test_sensor_integration(autoflux_system):
    """Test sensor integration in system."""
    autoflux_system.initialize()
    
    # Read all sensors
    sensor_data = autoflux_system.sensor_manager.read_all_sensors()
    
    assert sensor_data is not None
    assert len(sensor_data) > 0


def test_diagnostic_integration(autoflux_system):
    """Test diagnostic integration in system."""
    autoflux_system.initialize()
    
    system_state = {
        "sensors": {},
        "can_bus": {"connected": True, "error_count": 0},
        "control": autoflux_system.vehicle_controller.get_control_status(),
    }
    
    reports = autoflux_system.diagnostic_system.run_full_diagnostics(system_state)
    
    assert reports is not None
    assert len(reports) > 0


def test_inference_integration(autoflux_system):
    """Test inference integration in system."""
    import numpy as np
    
    autoflux_system.initialize()
    
    # Create test image
    image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    
    # Run inference
    result = autoflux_system.inference_engine.run_object_detection(image)
    
    assert result is not None
    assert result.predictions is not None
