"""
System Orchestrator

Coordinates all system components and manages the main control loop.
"""

import logging
import time
from typing import Dict, Optional
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)


class SystemOrchestrator:
    """
    Orchestrates the autonomous vehicle and NeuroFlux systems.
    
    Responsible for:
    - Main control loop
    - Data flow coordination
    - Component synchronization
    - Decision making
    """
    
    def __init__(
        self,
        config: Dict,
        sensor_manager,
        diagnostic_system,
        vehicle_controller,
        inference_engine,
        data_preprocessor,
    ):
        """
        Initialize system orchestrator.
        
        Args:
            config: Orchestrator configuration
            sensor_manager: Sensor manager instance
            diagnostic_system: Diagnostic system instance
            vehicle_controller: Vehicle controller instance
            inference_engine: Inference engine instance
            data_preprocessor: Data preprocessor instance
        """
        self.config = config
        self.sensor_manager = sensor_manager
        self.diagnostic_system = diagnostic_system
        self.vehicle_controller = vehicle_controller
        self.inference_engine = inference_engine
        self.data_preprocessor = data_preprocessor
        
        system_config = config.get("system", {})
        self.update_rate_hz = system_config.get("update_rate_hz", 30)
        self.update_period = 1.0 / self.update_rate_hz
        
        self.running = False
        self.emergency_mode = False
        self.cycle_count = 0
        
        logger.info(f"System orchestrator initialized at {self.update_rate_hz} Hz")
    
    def start(self):
        """Start the orchestration loop."""
        self.running = True
        logger.info("Orchestrator started")
        
        # In a real implementation, this would run in a separate thread
        # For now, we'll just log that it's ready
        logger.info("Orchestrator ready for processing")
    
    def stop(self):
        """Stop the orchestration loop."""
        self.running = False
        logger.info("Orchestrator stopped")
    
    def process_cycle(self):
        """
        Execute one processing cycle.
        
        This is the main control loop that:
        1. Reads sensor data
        2. Runs diagnostics
        3. Performs AI inference
        4. Makes control decisions
        5. Executes vehicle commands
        """
        cycle_start = time.time()
        
        try:
            # Step 1: Read sensor data
            sensor_data = self.sensor_manager.read_all_sensors()
            
            # Step 2: Run diagnostics
            # Safely serialize sensor data
            sensors_dict = {}
            for name, data in sensor_data.items():
                if data is not None and hasattr(data, '__dict__'):
                    sensors_dict[name] = data.__dict__
                else:
                    sensors_dict[name] = None
            
            system_state = {
                "sensors": sensors_dict,
                "control": self.vehicle_controller.get_control_status(),
                "can_bus": {"connected": True, "error_count": 0},
            }
            
            diagnostic_reports = self.diagnostic_system.run_full_diagnostics(
                system_state
            )
            
            # Check for critical issues
            critical_issues = self.diagnostic_system.get_critical_issues()
            if critical_issues:
                logger.warning(f"Critical issues detected: {len(critical_issues)}")
                self.handle_critical_issues(critical_issues)
            
            # Step 3: Run AI inference (if camera data available)
            inference_results = {}
            for sensor_name, data in sensor_data.items():
                if sensor_name.startswith("camera") and data:
                    # Simulate image data
                    image = np.zeros((1080, 1920, 3), dtype=np.uint8)
                    
                    # Run object detection
                    detection_result = self.inference_engine.run_object_detection(
                        image
                    )
                    inference_results["detection"] = detection_result
                    
                    # Run lane detection
                    lane_result = self.inference_engine.run_lane_detection(image)
                    inference_results["lanes"] = lane_result
                    
                    break  # Process one camera for now
            
            # Step 4: Make control decisions
            control_command = self.make_control_decision(
                sensor_data,
                inference_results,
                diagnostic_reports
            )
            
            # Step 5: Execute control command
            if control_command and not self.emergency_mode:
                self.vehicle_controller.execute_command(control_command)
            
            # Update cycle count
            self.cycle_count += 1
            
            # Log periodic status
            if self.cycle_count % (self.update_rate_hz * 10) == 0:  # Every 10 seconds
                self._log_status()
        
        except Exception as e:
            logger.error(f"Error in processing cycle: {e}", exc_info=True)
        
        # Calculate cycle time
        cycle_time = time.time() - cycle_start
        
        if cycle_time > self.update_period:
            logger.warning(
                f"Cycle time ({cycle_time:.3f}s) exceeded period "
                f"({self.update_period:.3f}s)"
            )
    
    def make_control_decision(
        self,
        sensor_data: Dict,
        inference_results: Dict,
        diagnostic_reports: list
    ):
        """
        Make vehicle control decision based on sensor data and AI inference.
        
        Args:
            sensor_data: Sensor readings
            inference_results: AI inference results
            diagnostic_reports: Diagnostic reports
            
        Returns:
            Control command or None
        """
        from src.autonomous_vehicle.control import ControlCommand
        
        # Simple decision logic (placeholder)
        # In a real implementation, this would be much more sophisticated
        
        # Check if we have detections
        detections = inference_results.get("detection")
        lanes = inference_results.get("lanes")
        
        # Default: maintain current state
        steering = 0.0
        throttle = 0.0
        brake = 0.0
        
        # If objects detected, adjust behavior
        if detections and detections.predictions:
            for det in detections.predictions:
                if det.get("class") == "pedestrian":
                    # Pedestrian detected, slow down
                    brake = 0.3
                    throttle = 0.0
                    logger.debug("Pedestrian detected, braking")
                    break
        
        # Follow lanes if detected
        if lanes and lanes.predictions.get("lanes"):
            # Simple lane following logic
            lane_data = lanes.predictions["lanes"]
            if len(lane_data) >= 2:
                # Center between lanes
                steering = 0.0  # Simplified
        
        return ControlCommand(
            steering_angle=steering,
            throttle=throttle,
            brake=brake,
            timestamp=time.time()
        )
    
    def handle_critical_issues(self, issues: list):
        """
        Handle critical diagnostic issues.
        
        Args:
            issues: List of critical diagnostic reports
        """
        logger.critical(f"Handling {len(issues)} critical issues")
        
        # Check if any issue requires emergency stop
        for issue in issues:
            if "control" in issue.component.lower():
                logger.critical("Control system issue, triggering emergency stop")
                self.emergency_stop()
                break
    
    def emergency_stop(self):
        """Trigger emergency stop mode."""
        logger.critical("EMERGENCY STOP MODE ACTIVATED")
        self.emergency_mode = True
        self.vehicle_controller.emergency_brake()
    
    def _log_status(self):
        """Log periodic status update."""
        inference_stats = self.inference_engine.get_performance_stats()
        health = self.diagnostic_system.get_system_health_summary()
        
        logger.info(
            f"Status: cycles={self.cycle_count}, "
            f"health={health['status']}, "
            f"inference_fps={inference_stats['fps']:.1f}"
        )
    
    def get_orchestrator_status(self) -> Dict:
        """
        Get orchestrator status.
        
        Returns:
            Dictionary with status information
        """
        return {
            "running": self.running,
            "emergency_mode": self.emergency_mode,
            "cycle_count": self.cycle_count,
            "update_rate_hz": self.update_rate_hz,
        }
