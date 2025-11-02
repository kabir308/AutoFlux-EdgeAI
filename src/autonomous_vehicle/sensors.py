"""
Sensor Management System

Manages all vehicle sensors (LiDAR, cameras, radar, GPS, IMU).
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class SensorType(Enum):
    """Types of sensors"""
    LIDAR = "lidar"
    CAMERA = "camera"
    RADAR = "radar"
    GPS = "gps"
    IMU = "imu"


@dataclass
class SensorData:
    """Generic sensor data structure"""
    sensor_type: SensorType
    timestamp: datetime
    data: Any
    status: str = "ok"
    error_msg: Optional[str] = None


class SensorManager:
    """
    Manages all vehicle sensors.
    
    Responsible for:
    - Sensor initialization and configuration
    - Data collection from all sensors
    - Sensor health monitoring
    - Data synchronization
    """
    
    def __init__(self, config: Dict):
        """
        Initialize sensor manager.
        
        Args:
            config: Sensor configuration dictionary
        """
        self.config = config
        self.sensors: Dict[str, Dict] = {}
        self.latest_data: Dict[str, SensorData] = {}
        
        # Initialize sensors based on configuration
        self._initialize_sensors()
        
        logger.info(f"Sensor manager initialized with {len(self.sensors)} sensors")
    
    def _initialize_sensors(self):
        """Initialize all configured sensors."""
        sensor_config = self.config.get("sensors", {})
        
        # Initialize LiDAR
        if sensor_config.get("lidar", {}).get("enabled"):
            self.sensors["lidar"] = {
                "type": SensorType.LIDAR,
                "config": sensor_config["lidar"],
                "status": "initialized"
            }
            logger.info("LiDAR sensor initialized")
        
        # Initialize cameras
        if sensor_config.get("camera", {}).get("enabled"):
            num_cameras = sensor_config["camera"].get("num_cameras", 1)
            for i in range(num_cameras):
                sensor_name = f"camera_{i}"
                self.sensors[sensor_name] = {
                    "type": SensorType.CAMERA,
                    "config": sensor_config["camera"],
                    "status": "initialized"
                }
            logger.info(f"Initialized {num_cameras} camera sensor(s)")
        
        # Initialize radar
        if sensor_config.get("radar", {}).get("enabled"):
            self.sensors["radar"] = {
                "type": SensorType.RADAR,
                "config": sensor_config["radar"],
                "status": "initialized"
            }
            logger.info("Radar sensor initialized")
        
        # Initialize GPS
        if sensor_config.get("gps", {}).get("enabled"):
            self.sensors["gps"] = {
                "type": SensorType.GPS,
                "config": sensor_config["gps"],
                "status": "initialized"
            }
            logger.info("GPS sensor initialized")
        
        # Initialize IMU
        if sensor_config.get("imu", {}).get("enabled"):
            self.sensors["imu"] = {
                "type": SensorType.IMU,
                "config": sensor_config["imu"],
                "status": "initialized"
            }
            logger.info("IMU sensor initialized")
    
    def read_lidar(self) -> Optional[SensorData]:
        """
        Read LiDAR sensor data.
        
        Returns:
            SensorData with LiDAR point cloud
        """
        if "lidar" not in self.sensors:
            return None
        
        # Simulate LiDAR data (in real implementation, read from hardware)
        data = {
            "points": [],  # Point cloud would be here
            "num_points": 0,
            "range_m": self.sensors["lidar"]["config"].get("max_range_m", 200),
            "channels": self.sensors["lidar"]["config"].get("num_channels", 64),
        }
        
        sensor_data = SensorData(
            sensor_type=SensorType.LIDAR,
            timestamp=datetime.now(),
            data=data,
            status="ok"
        )
        
        self.latest_data["lidar"] = sensor_data
        return sensor_data
    
    def read_camera(self, camera_id: int = 0) -> Optional[SensorData]:
        """
        Read camera sensor data.
        
        Args:
            camera_id: Camera identifier
            
        Returns:
            SensorData with camera image
        """
        sensor_name = f"camera_{camera_id}"
        if sensor_name not in self.sensors:
            return None
        
        # Simulate camera data (in real implementation, read from camera)
        config = self.sensors[sensor_name]["config"]
        data = {
            "image": None,  # Image array would be here
            "resolution": config.get("resolution", [1920, 1080]),
            "fps": config.get("fps", 30),
            "camera_id": camera_id,
        }
        
        sensor_data = SensorData(
            sensor_type=SensorType.CAMERA,
            timestamp=datetime.now(),
            data=data,
            status="ok"
        )
        
        self.latest_data[sensor_name] = sensor_data
        return sensor_data
    
    def read_radar(self) -> Optional[SensorData]:
        """
        Read radar sensor data.
        
        Returns:
            SensorData with radar detections
        """
        if "radar" not in self.sensors:
            return None
        
        # Simulate radar data
        data = {
            "detections": [],  # Radar detections would be here
            "num_detections": 0,
            "max_range_m": self.sensors["radar"]["config"].get("max_range_m", 150),
        }
        
        sensor_data = SensorData(
            sensor_type=SensorType.RADAR,
            timestamp=datetime.now(),
            data=data,
            status="ok"
        )
        
        self.latest_data["radar"] = sensor_data
        return sensor_data
    
    def read_gps(self) -> Optional[SensorData]:
        """
        Read GPS sensor data.
        
        Returns:
            SensorData with GPS position
        """
        if "gps" not in self.sensors:
            return None
        
        # Simulate GPS data
        data = {
            "latitude": 0.0,
            "longitude": 0.0,
            "altitude": 0.0,
            "accuracy": 2.5,  # meters
            "satellites": 12,
        }
        
        sensor_data = SensorData(
            sensor_type=SensorType.GPS,
            timestamp=datetime.now(),
            data=data,
            status="ok"
        )
        
        self.latest_data["gps"] = sensor_data
        return sensor_data
    
    def read_imu(self) -> Optional[SensorData]:
        """
        Read IMU sensor data.
        
        Returns:
            SensorData with IMU measurements
        """
        if "imu" not in self.sensors:
            return None
        
        # Simulate IMU data
        data = {
            "acceleration": [0.0, 0.0, 9.81],  # m/s^2
            "gyroscope": [0.0, 0.0, 0.0],  # rad/s
            "magnetometer": [0.0, 0.0, 0.0],  # μT
        }
        
        sensor_data = SensorData(
            sensor_type=SensorType.IMU,
            timestamp=datetime.now(),
            data=data,
            status="ok"
        )
        
        self.latest_data["imu"] = sensor_data
        return sensor_data
    
    def read_all_sensors(self) -> Dict[str, SensorData]:
        """
        Read data from all active sensors.
        
        Returns:
            Dictionary mapping sensor names to sensor data
        """
        sensor_data = {}
        
        # Read LiDAR
        if "lidar" in self.sensors:
            sensor_data["lidar"] = self.read_lidar()
        
        # Read all cameras
        for sensor_name in self.sensors:
            if sensor_name.startswith("camera_"):
                camera_id = int(sensor_name.split("_")[1])
                sensor_data[sensor_name] = self.read_camera(camera_id)
        
        # Read radar
        if "radar" in self.sensors:
            sensor_data["radar"] = self.read_radar()
        
        # Read GPS
        if "gps" in self.sensors:
            sensor_data["gps"] = self.read_gps()
        
        # Read IMU
        if "imu" in self.sensors:
            sensor_data["imu"] = self.read_imu()
        
        return sensor_data
    
    def get_sensor_status(self) -> Dict:
        """
        Get status of all sensors.
        
        Returns:
            Dictionary with sensor status information
        """
        status = {}
        
        for sensor_name, sensor_info in self.sensors.items():
            latest = self.latest_data.get(sensor_name)
            
            status[sensor_name] = {
                "type": sensor_info["type"].value,
                "status": sensor_info["status"],
                "last_update": latest.timestamp if latest else None,
                "data_available": latest is not None,
            }
        
        return status
    
    def get_synchronized_data(self, max_age_ms: float = 100) -> Optional[Dict]:
        """
        Get temporally synchronized sensor data.
        
        Args:
            max_age_ms: Maximum age difference between sensors in milliseconds
            
        Returns:
            Dictionary of synchronized sensor data or None if not available
        """
        if not self.latest_data:
            return None
        
        # Find the most recent timestamp
        timestamps = [data.timestamp for data in self.latest_data.values()]
        latest_time = max(timestamps)
        
        # Check if all sensors are within the time window
        synchronized = {}
        for sensor_name, data in self.latest_data.items():
            age_ms = (latest_time - data.timestamp).total_seconds() * 1000
            
            if age_ms <= max_age_ms:
                synchronized[sensor_name] = data
            else:
                logger.warning(
                    f"Sensor {sensor_name} data too old ({age_ms:.1f}ms), "
                    f"skipping synchronization"
                )
                return None
        
        return synchronized if len(synchronized) == len(self.latest_data) else None
