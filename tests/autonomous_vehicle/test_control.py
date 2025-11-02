"""
Unit tests for the Vehicle Controller.
"""

import pytest
from src.autonomous_vehicle.control import (
    VehicleController,
    ControlMode,
    ControlCommand,
    VehicleState,
)


@pytest.fixture
def control_config():
    """Vehicle controller configuration fixture."""
    return {
        "mode": "assisted",
        "max_speed_mps": 30.0,
        "max_acceleration_mps2": 3.0,
        "max_deceleration_mps2": 5.0,
        "max_steering_angle_deg": 45.0,
    }


@pytest.fixture
def controller(control_config):
    """Vehicle controller fixture."""
    return VehicleController(control_config)


def test_controller_initialization(controller):
    """Test controller initializes correctly."""
    assert controller.mode == ControlMode.ASSISTED
    assert controller.max_speed == 30.0
    assert controller.max_steering_angle == 45.0
    assert controller.emergency_stop is False


def test_set_control_mode(controller):
    """Test setting control mode."""
    controller.set_control_mode(ControlMode.AUTONOMOUS)
    assert controller.mode == ControlMode.AUTONOMOUS


def test_apply_safety_constraints_steering(controller):
    """Test safety constraints on steering."""
    # Steering too large
    command = ControlCommand(
        steering_angle=60.0,  # Exceeds max of 45
        throttle=0.5,
        brake=0.0,
        timestamp=0.0
    )
    
    safe_command = controller.apply_safety_constraints(command)
    
    assert safe_command.steering_angle == 45.0


def test_apply_safety_constraints_throttle_and_brake(controller):
    """Test that throttle and brake cannot both be active."""
    command = ControlCommand(
        steering_angle=0.0,
        throttle=0.5,
        brake=0.5,
        timestamp=0.0
    )
    
    safe_command = controller.apply_safety_constraints(command)
    
    # Brake should be prioritized
    assert safe_command.throttle == 0.0
    assert safe_command.brake == 0.5


def test_execute_command_success(controller):
    """Test successful command execution."""
    command = ControlCommand(
        steering_angle=10.0,
        throttle=0.3,
        brake=0.0,
        timestamp=0.0
    )
    
    success = controller.execute_command(command)
    
    assert success is True
    assert controller.current_command is not None
    assert controller.current_command.steering_angle == 10.0


def test_execute_command_during_emergency_stop(controller):
    """Test that commands are blocked during emergency stop."""
    controller.emergency_stop = True
    
    command = ControlCommand(
        steering_angle=10.0,
        throttle=0.3,
        brake=0.0,
        timestamp=0.0
    )
    
    success = controller.execute_command(command)
    
    assert success is False


def test_emergency_brake(controller):
    """Test emergency brake activation."""
    controller.emergency_brake()
    
    assert controller.emergency_stop is True
    assert controller.current_command is not None
    assert controller.current_command.brake == 1.0
    assert controller.current_command.throttle == 0.0


def test_release_emergency_stop(controller):
    """Test releasing emergency stop."""
    controller.emergency_stop = True
    controller.release_emergency_stop()
    
    assert controller.emergency_stop is False


def test_update_vehicle_state(controller):
    """Test updating vehicle state."""
    state = VehicleState(
        speed_mps=15.0,
        acceleration_mps2=1.0,
        steering_angle=5.0,
        position=(45.5, -73.6),
        heading=90.0
    )
    
    controller.update_vehicle_state(state)
    
    assert controller.vehicle_state == state


def test_get_control_status(controller):
    """Test getting control status."""
    status = controller.get_control_status()
    
    assert "mode" in status
    assert "emergency_stop" in status
    assert status["mode"] == "assisted"


def test_calculate_steering_command(controller):
    """Test steering calculation."""
    steering = controller.calculate_steering_command(
        target_heading=90.0,
        current_heading=80.0,
        speed_mps=10.0
    )
    
    # Should steer right (positive)
    assert steering > 0
    assert abs(steering) <= controller.max_steering_angle


def test_calculate_steering_command_wraparound(controller):
    """Test steering with heading wraparound."""
    steering = controller.calculate_steering_command(
        target_heading=10.0,
        current_heading=350.0,
        speed_mps=10.0
    )
    
    # Should take shortest path (20 degrees right)
    assert steering > 0


def test_calculate_speed_command_accelerate(controller):
    """Test speed calculation when accelerating."""
    throttle, brake = controller.calculate_speed_command(
        target_speed_mps=20.0,
        current_speed_mps=10.0
    )
    
    assert throttle > 0
    assert brake == 0.0


def test_calculate_speed_command_decelerate(controller):
    """Test speed calculation when decelerating."""
    throttle, brake = controller.calculate_speed_command(
        target_speed_mps=10.0,
        current_speed_mps=20.0
    )
    
    assert throttle == 0.0
    assert brake > 0


def test_calculate_speed_command_maintain(controller):
    """Test speed calculation when maintaining speed."""
    throttle, brake = controller.calculate_speed_command(
        target_speed_mps=15.0,
        current_speed_mps=15.2
    )
    
    # Small error should result in no action
    assert throttle == 0.0
    assert brake == 0.0
