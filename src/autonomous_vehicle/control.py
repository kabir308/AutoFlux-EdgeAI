"""
Vehicle Control System

Manages steering, acceleration, braking, and vehicle dynamics.
"""

import logging
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ControlMode(Enum):
    """Vehicle control modes"""
    MANUAL = "manual"
    ASSISTED = "assisted"
    AUTONOMOUS = "autonomous"


@dataclass
class ControlCommand:
    """Vehicle control command"""
    steering_angle: float  # degrees, -45 to +45
    throttle: float  # 0.0 to 1.0
    brake: float  # 0.0 to 1.0
    timestamp: float


@dataclass
class VehicleState:
    """Current vehicle state"""
    speed_mps: float
    acceleration_mps2: float
    steering_angle: float
    position: tuple  # (latitude, longitude)
    heading: float  # degrees


class VehicleController:
    """
    Main vehicle control system.
    
    Responsible for:
    - Steering control
    - Acceleration/braking control
    - Safety constraints enforcement
    - Control mode management
    """
    
    def __init__(self, config: Dict):
        """
        Initialize vehicle controller.
        
        Args:
            config: Control system configuration
        """
        self.config = config
        self.mode = ControlMode(config.get("mode", "assisted"))
        self.max_speed = config.get("max_speed_mps", 30.0)
        self.max_acceleration = config.get("max_acceleration_mps2", 3.0)
        self.max_deceleration = config.get("max_deceleration_mps2", 5.0)
        self.max_steering_angle = config.get("max_steering_angle_deg", 45.0)
        
        self.current_command: Optional[ControlCommand] = None
        self.vehicle_state: Optional[VehicleState] = None
        self.emergency_stop = False
        
        logger.info(f"Vehicle controller initialized in {self.mode.value} mode")
    
    def set_control_mode(self, mode: ControlMode):
        """
        Set vehicle control mode.
        
        Args:
            mode: New control mode
        """
        logger.info(f"Changing control mode from {self.mode.value} to {mode.value}")
        self.mode = mode
    
    def apply_safety_constraints(self, command: ControlCommand) -> ControlCommand:
        """
        Apply safety constraints to control command.
        
        Args:
            command: Requested control command
            
        Returns:
            Safety-constrained control command
        """
        # Constrain steering angle
        steering_angle = max(
            -self.max_steering_angle,
            min(self.max_steering_angle, command.steering_angle)
        )
        
        # Constrain throttle and brake
        throttle = max(0.0, min(1.0, command.throttle))
        brake = max(0.0, min(1.0, command.brake))
        
        # Cannot have both throttle and brake
        if throttle > 0 and brake > 0:
            logger.warning("Both throttle and brake commanded, prioritizing brake")
            throttle = 0.0
        
        return ControlCommand(
            steering_angle=steering_angle,
            throttle=throttle,
            brake=brake,
            timestamp=command.timestamp
        )
    
    def execute_command(self, command: ControlCommand) -> bool:
        """
        Execute vehicle control command.
        
        Args:
            command: Control command to execute
            
        Returns:
            True if command executed successfully
        """
        if self.emergency_stop:
            logger.warning("Emergency stop active, ignoring control command")
            return False
        
        # Apply safety constraints
        safe_command = self.apply_safety_constraints(command)
        
        # Check if command differs significantly from constrained version
        if abs(safe_command.steering_angle - command.steering_angle) > 1.0:
            logger.warning(
                f"Steering constrained: {command.steering_angle:.1f}° → "
                f"{safe_command.steering_angle:.1f}°"
            )
        
        # Store current command
        self.current_command = safe_command
        
        logger.debug(
            f"Executing command: steer={safe_command.steering_angle:.1f}°, "
            f"throttle={safe_command.throttle:.2f}, brake={safe_command.brake:.2f}"
        )
        
        return True
    
    def update_vehicle_state(self, state: VehicleState):
        """
        Update current vehicle state.
        
        Args:
            state: New vehicle state
        """
        self.vehicle_state = state
        
        # Check speed limit
        if state.speed_mps > self.max_speed:
            logger.warning(f"Speed limit exceeded: {state.speed_mps:.1f} m/s")
    
    def emergency_brake(self):
        """Activate emergency braking."""
        logger.critical("EMERGENCY BRAKE ACTIVATED")
        self.emergency_stop = True
        
        emergency_command = ControlCommand(
            steering_angle=0.0,
            throttle=0.0,
            brake=1.0,
            timestamp=0.0
        )
        
        self.current_command = emergency_command
    
    def release_emergency_stop(self):
        """Release emergency stop."""
        logger.info("Emergency stop released")
        self.emergency_stop = False
    
    def get_control_status(self) -> Dict:
        """
        Get current control system status.
        
        Returns:
            Dictionary with control status information
        """
        return {
            "mode": self.mode.value,
            "emergency_stop": self.emergency_stop,
            "current_command": {
                "steering": self.current_command.steering_angle if self.current_command else 0.0,
                "throttle": self.current_command.throttle if self.current_command else 0.0,
                "brake": self.current_command.brake if self.current_command else 0.0,
            } if self.current_command else None,
            "vehicle_state": {
                "speed_mps": self.vehicle_state.speed_mps if self.vehicle_state else 0.0,
                "steering_angle": self.vehicle_state.steering_angle if self.vehicle_state else 0.0,
            } if self.vehicle_state else None,
            "steering_responsive": not self.emergency_stop,
            "brakes_responsive": True,
            "actuator_errors": 0,
        }
    
    def calculate_steering_command(
        self,
        target_heading: float,
        current_heading: float,
        speed_mps: float
    ) -> float:
        """
        Calculate steering angle to reach target heading.
        
        Args:
            target_heading: Desired heading in degrees
            current_heading: Current heading in degrees
            speed_mps: Current vehicle speed
            
        Returns:
            Steering angle in degrees
        """
        # Calculate heading error
        heading_error = target_heading - current_heading
        
        # Normalize to -180 to +180
        while heading_error > 180:
            heading_error -= 360
        while heading_error < -180:
            heading_error += 360
        
        # Simple proportional control
        # Reduce gain at higher speeds for stability
        gain = 1.0 if speed_mps < 10 else 0.5
        steering_angle = heading_error * gain
        
        # Constrain to max steering angle
        steering_angle = max(
            -self.max_steering_angle,
            min(self.max_steering_angle, steering_angle)
        )
        
        return steering_angle
    
    def calculate_speed_command(
        self,
        target_speed_mps: float,
        current_speed_mps: float
    ) -> tuple:
        """
        Calculate throttle and brake to reach target speed.
        
        Args:
            target_speed_mps: Desired speed
            current_speed_mps: Current speed
            
        Returns:
            Tuple of (throttle, brake)
        """
        speed_error = target_speed_mps - current_speed_mps
        
        # If we need to slow down
        if speed_error < -0.5:
            throttle = 0.0
            brake = min(1.0, abs(speed_error) / 10.0)
        # If we need to speed up
        elif speed_error > 0.5:
            throttle = min(1.0, speed_error / 10.0)
            brake = 0.0
        # Maintain current speed
        else:
            throttle = 0.0
            brake = 0.0
        
        return throttle, brake
