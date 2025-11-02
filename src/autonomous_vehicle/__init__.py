"""
Module Véhicule Autonome - VOITURE-AUTONOME-ET-DIAGNOSTIC-

Ce module gère le diagnostic et le contrôle des véhicules autonomes.
"""

from src.autonomous_vehicle.diagnostics import DiagnosticSystem
from src.autonomous_vehicle.control import VehicleController
from src.autonomous_vehicle.sensors import SensorManager

__all__ = [
    "DiagnosticSystem",
    "VehicleController", 
    "SensorManager",
]
