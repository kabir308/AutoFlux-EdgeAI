"""
AutoFlux System - Main Integration Module

Coordinates the autonomous vehicle and NeuroFlux systems.
"""

import logging
from typing import Dict, Optional
import yaml
from pathlib import Path

from src.autonomous_vehicle import DiagnosticSystem, VehicleController, SensorManager
from src.neuroflux import InferenceEngine, ModelManager, DataPreprocessor
from src.integration.orchestrator import SystemOrchestrator

logger = logging.getLogger(__name__)


class AutoFluxSystem:
    """
    Main system class that integrates autonomous vehicle and NeuroFlux components.
    
    This is the unified architecture combining:
    - VOITURE-AUTONOME-ET-DIAGNOSTIC-: Vehicle diagnostics and control
    - NeuroFlux: Edge AI inference
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize AutoFlux system.
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.sensor_manager = None
        self.diagnostic_system = None
        self.vehicle_controller = None
        self.model_manager = None
        self.data_preprocessor = None
        self.inference_engine = None
        self.orchestrator = None
        
        self.running = False
        
        logger.info("AutoFlux-EdgeAI system created")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """
        Load system configuration.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        if config_path is None:
            config_path = "config/config.yaml"
        
        config_file = Path(config_path)
        
        if not config_file.exists():
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return self._get_default_config()
        
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration."""
        return {
            "autonomous_vehicle": {
                "sensors": {"lidar": {"enabled": False}},
                "control": {"mode": "manual"},
                "diagnostics": {"enabled": True},
            },
            "neuroflux": {
                "models": {},
                "hardware": {"accelerator": "cpu", "precision": "fp32"},
            },
            "integration": {
                "system": {"update_rate_hz": 30},
                "monitoring": {"log_level": "INFO"},
            },
        }
    
    def initialize(self):
        """Initialize all system components."""
        logger.info("Initializing AutoFlux system components...")
        
        # Initialize autonomous vehicle components
        av_config = self.config.get("autonomous_vehicle", {})
        
        self.sensor_manager = SensorManager(av_config)
        self.diagnostic_system = DiagnosticSystem(
            av_config.get("diagnostics", {})
        )
        self.vehicle_controller = VehicleController(
            av_config.get("control", {})
        )
        
        # Initialize NeuroFlux components
        nf_config = self.config.get("neuroflux", {})
        
        self.model_manager = ModelManager(nf_config)
        self.data_preprocessor = DataPreprocessor(nf_config)
        self.inference_engine = InferenceEngine(nf_config, self.model_manager)
        
        # Load models
        self.model_manager.load_all_models()
        
        # Initialize orchestrator
        self.orchestrator = SystemOrchestrator(
            config=self.config.get("integration", {}),
            sensor_manager=self.sensor_manager,
            diagnostic_system=self.diagnostic_system,
            vehicle_controller=self.vehicle_controller,
            inference_engine=self.inference_engine,
            data_preprocessor=self.data_preprocessor,
        )
        
        logger.info("AutoFlux system initialized successfully")
    
    def start(self):
        """Start the AutoFlux system."""
        if not self.orchestrator:
            self.initialize()
        
        logger.info("Starting AutoFlux system...")
        self.running = True
        
        # Start the orchestrator
        self.orchestrator.start()
        
        logger.info("AutoFlux system running")
    
    def stop(self):
        """Stop the AutoFlux system."""
        logger.info("Stopping AutoFlux system...")
        self.running = False
        
        if self.orchestrator:
            self.orchestrator.stop()
        
        logger.info("AutoFlux system stopped")
    
    def get_system_status(self) -> Dict:
        """
        Get overall system status.
        
        Returns:
            Dictionary with system status information
        """
        if not self.orchestrator:
            return {"status": "not_initialized"}
        
        return {
            "running": self.running,
            "sensors": self.sensor_manager.get_sensor_status() if self.sensor_manager else {},
            "diagnostics": self.diagnostic_system.get_system_health_summary() if self.diagnostic_system else {},
            "control": self.vehicle_controller.get_control_status() if self.vehicle_controller else {},
            "models": self.model_manager.get_model_metadata() if self.model_manager else {},
            "inference": self.inference_engine.get_performance_stats() if self.inference_engine else {},
        }
    
    def emergency_stop(self):
        """Trigger emergency stop."""
        logger.critical("EMERGENCY STOP TRIGGERED")
        
        if self.vehicle_controller:
            self.vehicle_controller.emergency_brake()
        
        if self.orchestrator:
            self.orchestrator.emergency_stop()
    
    def get_version(self) -> str:
        """Get system version."""
        return "1.0.0"
    
    def __repr__(self) -> str:
        """String representation of the system."""
        status = "running" if self.running else "stopped"
        return f"AutoFluxSystem(status={status}, version={self.get_version()})"
