---
layout: default
title: Packages et Dépendances
---

# 📦 Packages et Dépendances

## Vue d'ensemble des Packages

AutoFlux-EdgeAI est construit avec un ensemble soigneusement sélectionné de packages Python pour assurer performance, fiabilité et compatibilité.

---

## 🔧 Dépendances Principales

### Computing et Calcul Numérique

#### NumPy >= 1.21.0
- **Usage** : Calcul numérique, manipulation de tableaux
- **Modules** : NeuroFlux (preprocessing, inference)
- **Raison** : Foundation pour le calcul scientifique et l'IA

```python
# Utilisé dans preprocessing.py
import numpy as np
processed = (image - self.mean) / self.std
```

#### Pandas >= 1.3.0
- **Usage** : Manipulation de données, logging
- **Modules** : Data management, analytics
- **Raison** : Analyse efficace des données de capteurs

---

### Vision et Traitement d'Images

#### OpenCV-Python >= 4.5.0
- **Usage** : Traitement d'images, manipulation de frames caméra
- **Modules** : NeuroFlux (preprocessing), Autonomous Vehicle (sensors)
- **Raison** : Standard de l'industrie pour computer vision

```python
# Redimensionnement d'images
import cv2
resized = cv2.resize(image, (width, height))
```

---

### Deep Learning et IA

#### PyTorch >= 1.10.0
- **Usage** : Framework de deep learning
- **Modules** : NeuroFlux (models, training)
- **Raison** : Flexibilité et performance pour edge AI

#### TorchVision >= 0.11.0
- **Usage** : Transformations d'images, modèles pré-entraînés
- **Modules** : NeuroFlux (preprocessing, models)
- **Raison** : Utilitaires vision pour PyTorch

#### ONNX Runtime >= 1.10.0
- **Usage** : Inférence optimisée de modèles ONNX
- **Modules** : NeuroFlux (inference)
- **Raison** : Performance maximale sur edge devices

```python
# Chargement de modèle ONNX
import onnxruntime as ort
session = ort.InferenceSession(model_path)
```

---

### Véhicule et Communication

#### python-can >= 4.0.0
- **Usage** : Interface CAN bus pour communication véhicule
- **Modules** : Autonomous Vehicle (can_interface)
- **Raison** : Standard pour communication automobile

```python
# Configuration CAN
import can
bus = can.interface.Bus(channel='can0', bustype='socketcan')
```

---

### Web et API

#### FastAPI >= 0.70.0
- **Usage** : API REST pour monitoring et contrôle
- **Modules** : Integration (api)
- **Raison** : Performance et facilité d'utilisation

#### Uvicorn >= 0.15.0
- **Usage** : Serveur ASGI pour FastAPI
- **Modules** : Integration (api)
- **Raison** : Serveur async haute performance

#### Pydantic >= 1.9.0
- **Usage** : Validation de données, configuration
- **Modules** : Integration (api, system)
- **Raison** : Type safety et validation automatique

```python
# API endpoint
from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
async def get_status():
    return system.get_system_status()
```

---

### Configuration et Logging

#### PyYAML >= 6.0
- **Usage** : Lecture/écriture de fichiers de configuration
- **Modules** : Integration (system)
- **Raison** : Format de configuration standard

```python
# Chargement de configuration
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
```

---

## 🧪 Dépendances de Développement

### Testing

#### pytest >= 7.0.0
- **Usage** : Framework de tests unitaires et d'intégration
- **Tests** : 51 tests dans tests/
- **Raison** : Standard Python pour testing

#### pytest-asyncio >= 0.18.0
- **Usage** : Tests pour code asynchrone
- **Tests** : API et orchestrator tests
- **Raison** : Support async/await dans tests

#### pytest-cov >= 3.0.0
- **Usage** : Couverture de code
- **Tests** : Rapports de coverage
- **Raison** : Qualité et complétude des tests

```bash
# Exécuter tests avec couverture
pytest tests/ --cov=src --cov-report=html
```

---

### Code Quality

#### Black >= 22.0.0
- **Usage** : Formatage automatique du code
- **Raison** : Consistency et lisibilité

```bash
# Formater tout le code
black src/ tests/
```

#### Flake8 >= 4.0.0
- **Usage** : Linting et vérification de style
- **Raison** : Conformité PEP 8

```bash
# Vérifier le style
flake8 src/ tests/
```

#### MyPy >= 0.950
- **Usage** : Vérification de types statiques
- **Raison** : Type safety et réduction de bugs

```bash
# Vérifier les types
mypy src/
```

---

## 📊 Dépendances Optionnelles

### Accélération GPU

#### CUDA Toolkit
- **Usage** : Accélération GPU pour inférence
- **Version recommandée** : 11.3+
- **Modules** : NeuroFlux (inference)

#### TensorRT >= 8.0
- **Usage** : Optimisation d'inférence sur GPU NVIDIA
- **Modules** : NeuroFlux (optimization)
- **Installation** : Optionnelle, pour performance maximale

---

### Visualisation et Monitoring

#### Matplotlib >= 3.4.0
- **Usage** : Visualisation de données et métriques
- **Modules** : Analytics, debugging

#### Plotly >= 5.0.0
- **Usage** : Graphiques interactifs
- **Modules** : Dashboard, monitoring

---

## 🔄 Graphe de Dépendances

```
AutoFlux-EdgeAI
├── Core Computing
│   ├── numpy (1.21.0+)
│   └── pandas (1.3.0+)
│
├── Deep Learning
│   ├── torch (1.10.0+)
│   ├── torchvision (0.11.0+)
│   └── onnxruntime (1.10.0+)
│
├── Vision
│   └── opencv-python (4.5.0+)
│
├── Vehicle Interface
│   └── python-can (4.0.0+)
│
├── Web & API
│   ├── fastapi (0.70.0+)
│   ├── uvicorn (0.15.0+)
│   └── pydantic (1.9.0+)
│
├── Configuration
│   └── pyyaml (6.0+)
│
└── Development
    ├── pytest (7.0.0+)
    ├── pytest-asyncio (0.18.0+)
    ├── pytest-cov (3.0.0+)
    ├── black (22.0.0+)
    ├── flake8 (4.0.0+)
    └── mypy (0.950+)
```

---

## 📥 Installation des Packages

### Installation Standard

```bash
pip install -r requirements.txt
```

### Installation avec Package Manager

```bash
# Installation éditable pour développement
pip install -e .

# Avec dépendances de dev
pip install -e ".[dev]"
```

### Installation Conda (Alternatif)

```bash
conda env create -f environment.yml
conda activate autoflux-edgeai
```

---

## 🎯 Compatibilité

### Versions Python

- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ⚠️ Python 3.11 (en test)

### Systèmes d'Exploitation

- ✅ Linux (Ubuntu 18.04+, Debian 10+)
- ✅ macOS (10.15+)
- ✅ Windows 10/11 (avec adaptations)

### Architectures

- ✅ x86_64 (Intel/AMD)
- ✅ ARM64 (Raspberry Pi 4, NVIDIA Jetson)
- ⚠️ ARM32 (support limité)

---

## 🔐 Sécurité des Packages

Tous les packages sont vérifiés pour :

- ✅ **Vulnérabilités connues** (via `pip audit`)
- ✅ **Licences compatibles** (MIT, Apache 2.0, BSD)
- ✅ **Maintenance active** (mises à jour régulières)
- ✅ **Communauté stable** (GitHub stars, downloads)

### Vérification de Sécurité

```bash
# Vérifier les vulnérabilités
pip install pip-audit
pip-audit

# Mise à jour sécurisée
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

---

## 📈 Métriques de Performance

### Taille des Packages

| Package | Taille | Impact |
|---------|--------|--------|
| torch | ~750 MB | Élevé (inference) |
| opencv-python | ~100 MB | Moyen (preprocessing) |
| onnxruntime | ~40 MB | Faible (optimisé) |
| fastapi | ~5 MB | Minimal |
| Total | ~1 GB | Edge device compatible |

### Temps de Chargement

- **Import initial** : ~2-3 secondes
- **Chargement modèles** : ~1-2 secondes
- **Initialisation système** : ~1 seconde

---

## 🚀 Optimisations

### Pour Edge Devices

```bash
# Installation légère sans PyTorch complet
pip install onnxruntime-gpu  # ou onnxruntime
pip install opencv-python-headless  # Version sans GUI
```

### Pour Production

```bash
# Installation avec packages optimisés
pip install torch --index-url https://download.pytorch.org/whl/cu118
pip install onnxruntime-gpu
```

---

## 📝 Notes de Version

### Version 1.0.0

- ✅ Toutes les dépendances principales testées
- ✅ Compatibilité Python 3.8+
- ✅ Support multi-plateforme
- ✅ 0 vulnérabilités de sécurité

---

## 🔗 Ressources

- [PyPI - Python Package Index](https://pypi.org/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [ONNX Runtime](https://onnxruntime.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [python-can Documentation](https://python-can.readthedocs.io/)
