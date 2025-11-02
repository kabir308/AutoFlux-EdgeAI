"""
Basic example demonstrating the AutoFlux-EdgeAI system.

This example shows how to initialize and use the unified system.
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.integration import AutoFluxSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main example function."""
    logger.info("=" * 60)
    logger.info("AutoFlux-EdgeAI System - Basic Example")
    logger.info("=" * 60)
    
    # Create the system
    logger.info("\n1. Creating AutoFlux system...")
    system = AutoFluxSystem(config_path="config/config.yaml")
    
    # Initialize components
    logger.info("\n2. Initializing system components...")
    system.initialize()
    
    # Display system status
    logger.info("\n3. System status:")
    status = system.get_system_status()
    
    logger.info(f"   - Running: {status.get('running')}")
    logger.info(f"   - Sensors: {len(status.get('sensors', {}))} configured")
    logger.info(f"   - Models: {len(status.get('models', {}))} loaded")
    
    # Display sensor status
    logger.info("\n4. Sensor status:")
    for sensor_name, sensor_info in status.get('sensors', {}).items():
        logger.info(f"   - {sensor_name}: {sensor_info.get('status')}")
    
    # Display loaded models
    logger.info("\n5. Loaded models:")
    for model_name, model_info in status.get('models', {}).items():
        logger.info(
            f"   - {model_name}: "
            f"loaded={model_info.get('loaded')}, "
            f"simulation={model_info.get('simulation_mode')}"
        )
    
    # Start the system
    logger.info("\n6. Starting the system...")
    system.start()
    
    # Simulate one processing cycle
    logger.info("\n7. Processing one cycle...")
    if system.orchestrator:
        system.orchestrator.process_cycle()
    
    # Display performance stats
    logger.info("\n8. Performance statistics:")
    perf = status.get('inference', {})
    logger.info(f"   - Total inferences: {perf.get('total_inferences', 0)}")
    logger.info(f"   - Average time: {perf.get('average_time_ms', 0):.2f} ms")
    logger.info(f"   - FPS: {perf.get('fps', 0):.1f}")
    
    # Display diagnostic summary
    logger.info("\n9. Diagnostic summary:")
    diag = status.get('diagnostics', {})
    logger.info(f"   - Status: {diag.get('status', 'unknown')}")
    logger.info(f"   - Message: {diag.get('message', 'N/A')}")
    
    # Display control status
    logger.info("\n10. Control status:")
    control = status.get('control', {})
    logger.info(f"    - Mode: {control.get('mode', 'unknown')}")
    logger.info(f"    - Emergency stop: {control.get('emergency_stop', False)}")
    
    # Stop the system
    logger.info("\n11. Stopping the system...")
    system.stop()
    
    logger.info("\n" + "=" * 60)
    logger.info("Example completed successfully!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
