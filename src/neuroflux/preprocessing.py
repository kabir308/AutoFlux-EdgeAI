"""
Data Preprocessing for NeuroFlux

Handles preprocessing of sensor data for neural network inference.
"""

import logging
from typing import Dict, Tuple, Optional
import numpy as np

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Preprocesses sensor data for neural network inference.
    
    Responsible for:
    - Image normalization
    - Resizing and formatting
    - Data augmentation
    - Format conversion
    """
    
    def __init__(self, config: Dict):
        """
        Initialize data preprocessor.
        
        Args:
            config: Preprocessing configuration
        """
        self.config = config
        
        preprocessing_config = config.get("preprocessing", {})
        normalization = preprocessing_config.get("normalization", {})
        
        self.mean = np.array(normalization.get("mean", [0.485, 0.456, 0.406]))
        self.std = np.array(normalization.get("std", [0.229, 0.224, 0.225]))
        self.resize_method = preprocessing_config.get("resize_method", "bilinear")
        
        logger.info("Data preprocessor initialized")
    
    def preprocess_image(
        self,
        image: np.ndarray,
        target_size: Tuple[int, int],
        normalize: bool = True
    ) -> np.ndarray:
        """
        Preprocess image for neural network input.
        
        Args:
            image: Input image array (H, W, C)
            target_size: Target size (height, width)
            normalize: Whether to apply normalization
            
        Returns:
            Preprocessed image array
        """
        # Resize image
        resized = self._resize_image(image, target_size)
        
        # Convert to float and scale to [0, 1]
        processed = resized.astype(np.float32) / 255.0
        
        # Apply normalization if requested
        if normalize:
            processed = self._normalize_image(processed)
        
        # Convert to CHW format (channels first)
        if len(processed.shape) == 3:
            processed = np.transpose(processed, (2, 0, 1))
        
        # Add batch dimension
        processed = np.expand_dims(processed, axis=0)
        
        return processed
    
    def _resize_image(
        self,
        image: np.ndarray,
        target_size: Tuple[int, int]
    ) -> np.ndarray:
        """
        Resize image to target size.
        
        Args:
            image: Input image
            target_size: Target (height, width)
            
        Returns:
            Resized image
        """
        # Simple resize simulation (in real implementation, use cv2.resize)
        target_h, target_w = target_size
        
        if image.shape[:2] == target_size:
            return image
        
        # Placeholder: return image with target size
        # In real implementation: cv2.resize(image, (target_w, target_h))
        logger.debug(f"Resizing image from {image.shape[:2]} to {target_size}")
        
        # Return simulated resized image
        if len(image.shape) == 3:
            return np.zeros((target_h, target_w, image.shape[2]), dtype=image.dtype)
        else:
            return np.zeros((target_h, target_w), dtype=image.dtype)
    
    def _normalize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Normalize image using mean and standard deviation.
        
        Args:
            image: Input image in range [0, 1]
            
        Returns:
            Normalized image
        """
        # Apply ImageNet normalization
        normalized = (image - self.mean) / self.std
        return normalized.astype(np.float32)
    
    def preprocess_lidar(
        self,
        point_cloud: np.ndarray,
        max_points: int = 16384
    ) -> np.ndarray:
        """
        Preprocess LiDAR point cloud data.
        
        Args:
            point_cloud: Input point cloud (N, 3 or 4)
            max_points: Maximum number of points to keep
            
        Returns:
            Preprocessed point cloud
        """
        if len(point_cloud) == 0:
            return np.zeros((max_points, 3), dtype=np.float32)
        
        # Sample or pad to fixed size
        if len(point_cloud) > max_points:
            # Random sampling
            indices = np.random.choice(len(point_cloud), max_points, replace=False)
            sampled = point_cloud[indices]
        else:
            # Pad with zeros
            padding = max_points - len(point_cloud)
            sampled = np.vstack([
                point_cloud,
                np.zeros((padding, point_cloud.shape[1]))
            ])
        
        # Take only XYZ coordinates
        if sampled.shape[1] > 3:
            sampled = sampled[:, :3]
        
        return sampled.astype(np.float32)
    
    def preprocess_radar(self, radar_data: Dict) -> np.ndarray:
        """
        Preprocess radar detection data.
        
        Args:
            radar_data: Radar detection dictionary
            
        Returns:
            Preprocessed radar tensor
        """
        detections = radar_data.get("detections", [])
        
        # Convert detections to fixed-size array
        max_detections = 50
        radar_array = np.zeros((max_detections, 4), dtype=np.float32)
        
        for i, detection in enumerate(detections[:max_detections]):
            # Store: range, azimuth, elevation, velocity
            radar_array[i] = [
                detection.get("range", 0.0),
                detection.get("azimuth", 0.0),
                detection.get("elevation", 0.0),
                detection.get("velocity", 0.0),
            ]
        
        return radar_array
    
    def denormalize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Reverse normalization for visualization.
        
        Args:
            image: Normalized image
            
        Returns:
            Denormalized image in range [0, 255]
        """
        # Reverse normalization
        denormalized = (image * self.std) + self.mean
        
        # Scale to [0, 255]
        denormalized = np.clip(denormalized * 255.0, 0, 255)
        
        return denormalized.astype(np.uint8)
    
    def prepare_batch(
        self,
        images: list,
        target_size: Tuple[int, int]
    ) -> np.ndarray:
        """
        Prepare a batch of images for inference.
        
        Args:
            images: List of input images
            target_size: Target size for all images
            
        Returns:
            Batched and preprocessed images
        """
        batch = []
        
        for image in images:
            preprocessed = self.preprocess_image(image, target_size)
            batch.append(preprocessed[0])  # Remove batch dimension
        
        # Stack into batch
        return np.stack(batch, axis=0)
    
    def postprocess_detections(
        self,
        detections: np.ndarray,
        original_size: Tuple[int, int],
        target_size: Tuple[int, int]
    ) -> list:
        """
        Postprocess detection results to original image coordinates.
        
        Args:
            detections: Detection results
            original_size: Original image size
            target_size: Size used for inference
            
        Returns:
            Detections in original image coordinates
        """
        orig_h, orig_w = original_size
        target_h, target_w = target_size
        
        scale_x = orig_w / target_w
        scale_y = orig_h / target_h
        
        processed_detections = []
        
        for det in detections:
            if isinstance(det, dict) and "bbox" in det:
                bbox = det["bbox"]
                scaled_bbox = [
                    bbox[0] * scale_x,
                    bbox[1] * scale_y,
                    bbox[2] * scale_x,
                    bbox[3] * scale_y,
                ]
                
                processed_det = det.copy()
                processed_det["bbox"] = scaled_bbox
                processed_detections.append(processed_det)
        
        return processed_detections
