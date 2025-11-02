"""
Unit tests for NeuroFlux Inference Engine.
"""

import pytest
import numpy as np
from src.neuroflux.inference import InferenceEngine, InferenceResult
from src.neuroflux.models import ModelManager, ModelType


@pytest.fixture
def neuroflux_config():
    """NeuroFlux configuration fixture."""
    return {
        "models": {
            "object_detection": {
                "model_name": "yolov8n",
                "model_path": "models/yolov8n.onnx",
                "confidence_threshold": 0.5,
                "input_size": [640, 640],
            },
            "semantic_segmentation": {
                "model_name": "deeplabv3",
                "model_path": "models/deeplabv3.onnx",
                "num_classes": 20,
                "input_size": [512, 512],
            },
            "lane_detection": {
                "model_name": "ufld",
                "model_path": "models/ufld.onnx",
                "input_size": [800, 288],
            },
        },
        "hardware": {
            "accelerator": "cpu",
            "precision": "fp32",
            "batch_size": 1,
        },
    }


@pytest.fixture
def model_manager(neuroflux_config):
    """Model manager fixture."""
    manager = ModelManager(neuroflux_config)
    manager.load_all_models()
    return manager


@pytest.fixture
def inference_engine(neuroflux_config, model_manager):
    """Inference engine fixture."""
    return InferenceEngine(neuroflux_config, model_manager)


def test_inference_engine_initialization(inference_engine):
    """Test inference engine initializes correctly."""
    assert inference_engine.accelerator == "cpu"
    assert inference_engine.precision == "fp32"
    assert inference_engine.batch_size == 1


def test_run_object_detection(inference_engine):
    """Test object detection inference."""
    image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    
    result = inference_engine.run_object_detection(image)
    
    assert isinstance(result, InferenceResult)
    assert result.model_type == ModelType.OBJECT_DETECTION
    assert result.predictions is not None
    assert result.inference_time_ms >= 0


def test_run_object_detection_with_threshold(inference_engine):
    """Test object detection with custom threshold."""
    image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    
    result = inference_engine.run_object_detection(image, confidence_threshold=0.7)
    
    assert result.confidence == 0.7


def test_run_segmentation(inference_engine):
    """Test semantic segmentation inference."""
    image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    
    result = inference_engine.run_segmentation(image)
    
    assert isinstance(result, InferenceResult)
    assert result.model_type == ModelType.SEMANTIC_SEGMENTATION
    assert result.predictions is not None


def test_run_lane_detection(inference_engine):
    """Test lane detection inference."""
    image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    
    result = inference_engine.run_lane_detection(image)
    
    assert isinstance(result, InferenceResult)
    assert result.model_type == ModelType.LANE_DETECTION
    assert result.predictions is not None


def test_performance_stats(inference_engine):
    """Test performance statistics tracking."""
    image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    
    # Run multiple inferences
    for _ in range(5):
        inference_engine.run_object_detection(image)
    
    stats = inference_engine.get_performance_stats()
    
    assert stats["total_inferences"] == 5
    assert stats["total_time_ms"] > 0
    assert stats["average_time_ms"] > 0
    assert stats["fps"] > 0
    assert stats["accelerator"] == "cpu"


def test_reset_stats(inference_engine):
    """Test resetting performance statistics."""
    image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    
    inference_engine.run_object_detection(image)
    
    assert inference_engine.inference_count > 0
    
    inference_engine.reset_stats()
    
    assert inference_engine.inference_count == 0
    assert inference_engine.total_inference_time == 0.0


def test_simulate_object_detection(inference_engine):
    """Test simulated object detection."""
    detections = inference_engine._simulate_object_detection(0.5)
    
    assert isinstance(detections, list)
    assert len(detections) > 0
    assert all("class" in d for d in detections)
    assert all("confidence" in d for d in detections)
    assert all("bbox" in d for d in detections)


def test_simulate_segmentation(inference_engine):
    """Test simulated segmentation."""
    image = np.zeros((512, 512, 3), dtype=np.uint8)
    segmentation = inference_engine._simulate_segmentation(image)
    
    assert isinstance(segmentation, dict)
    assert "mask" in segmentation
    assert "classes" in segmentation


def test_simulate_lane_detection(inference_engine):
    """Test simulated lane detection."""
    lanes = inference_engine._simulate_lane_detection()
    
    assert isinstance(lanes, dict)
    assert "lanes" in lanes
    assert "num_lanes" in lanes
    assert lanes["num_lanes"] > 0
