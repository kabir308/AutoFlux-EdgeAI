"""
API Manager for AutoFlux System

Provides REST API for system monitoring and control.
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class APIManager:
    """
    Manages REST API for AutoFlux system.
    
    Provides endpoints for:
    - System status monitoring
    - Configuration management
    - Control commands
    - Diagnostic access
    """
    
    def __init__(self, config: Dict, system):
        """
        Initialize API manager.
        
        Args:
            config: API configuration
            system: AutoFluxSystem instance
        """
        self.config = config
        self.system = system
        
        api_config = config.get("api", {})
        self.enabled = api_config.get("enabled", True)
        self.host = api_config.get("host", "0.0.0.0")
        self.port = api_config.get("port", 8000)
        self.workers = api_config.get("workers", 4)
        
        self.app = None
        
        if self.enabled:
            self._setup_api()
        
        logger.info(f"API manager initialized on {self.host}:{self.port}")
    
    def _setup_api(self):
        """Setup FastAPI application and routes."""
        try:
            from fastapi import FastAPI
            
            self.app = FastAPI(
                title="AutoFlux-EdgeAI API",
                description="Unified API for autonomous vehicle and edge AI system",
                version="1.0.0"
            )
            
            self._register_routes()
            
        except ImportError:
            logger.warning("FastAPI not available, API disabled")
            self.enabled = False
    
    def _register_routes(self):
        """Register API routes."""
        if not self.app:
            return
        
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {
                "name": "AutoFlux-EdgeAI",
                "version": self.system.get_version(),
                "status": "running" if self.system.running else "stopped"
            }
        
        @self.app.get("/status")
        async def get_status():
            """Get system status."""
            return self.system.get_system_status()
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            status = self.system.get_system_status()
            
            if status.get("running"):
                return {"status": "healthy"}
            else:
                return {"status": "unhealthy"}
        
        @self.app.post("/emergency-stop")
        async def emergency_stop():
            """Trigger emergency stop."""
            self.system.emergency_stop()
            return {"status": "emergency_stop_activated"}
        
        @self.app.get("/sensors")
        async def get_sensors():
            """Get sensor status."""
            if self.system.sensor_manager:
                return self.system.sensor_manager.get_sensor_status()
            return {}
        
        @self.app.get("/diagnostics")
        async def get_diagnostics():
            """Get diagnostic summary."""
            if self.system.diagnostic_system:
                return self.system.diagnostic_system.get_system_health_summary()
            return {}
        
        @self.app.get("/models")
        async def get_models():
            """Get loaded models information."""
            if self.system.model_manager:
                return self.system.model_manager.get_model_metadata()
            return {}
        
        @self.app.get("/performance")
        async def get_performance():
            """Get inference performance statistics."""
            if self.system.inference_engine:
                return self.system.inference_engine.get_performance_stats()
            return {}
    
    def start(self):
        """Start the API server."""
        if not self.enabled or not self.app:
            logger.info("API not enabled")
            return
        
        logger.info(f"Starting API server on {self.host}:{self.port}")
        
        # In a real implementation, start uvicorn server
        # import uvicorn
        # uvicorn.run(self.app, host=self.host, port=self.port, workers=self.workers)
    
    def stop(self):
        """Stop the API server."""
        logger.info("API server stopped")
