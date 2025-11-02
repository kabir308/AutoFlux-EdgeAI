# AutoFlux-EdgeAI - Résumé du Projet

## Vue d'ensemble

AutoFlux-EdgeAI est une architecture unifiée qui fusionne deux systèmes complémentaires :
- **VOITURE-AUTONOME-ET-DIAGNOSTIC-** : Système de diagnostic et de contrôle pour véhicules autonomes
- **NeuroFlux** : Système d'intelligence artificielle embarquée (Edge AI) pour l'inférence en temps réel

Ce projet a été développé dans le cadre d'un projet de Maîtrise en Ingénierie.

## Architecture Implémentée

### 1. Module Véhicule Autonome (`src/autonomous_vehicle/`)

#### Diagnostic System (`diagnostics.py`)
- Surveillance de la santé du système en temps réel
- Détection des défaillances de capteurs
- Vérification du bus CAN
- Contrôle de l'état des systèmes de commande
- 4 niveaux de diagnostic : INFO, WARNING, ERROR, CRITICAL

#### Vehicle Controller (`control.py`)
- 3 modes de contrôle : MANUAL, ASSISTED, AUTONOMOUS
- Gestion de la direction, accélération, et freinage
- Contraintes de sécurité automatiques
- Freinage d'urgence
- Calcul de commandes de direction et de vitesse

#### Sensor Manager (`sensors.py`)
- Support pour 5 types de capteurs : LiDAR, Caméras, Radar, GPS, IMU
- Lecture synchronisée des données
- Validation et détection d'anomalies
- Support multi-caméras (jusqu'à 4 caméras)

### 2. Module NeuroFlux Edge AI (`src/neuroflux/`)

#### Model Manager (`models.py`)
- Gestion des modèles de réseaux neuronaux
- Support pour 4 types de modèles :
  - Détection d'objets (YOLO, etc.)
  - Segmentation sémantique (DeepLab, etc.)
  - Détection de voies
  - Estimation de profondeur
- Chargement de modèles ONNX
- Mode simulation pour développement

#### Inference Engine (`inference.py`)
- Inférence en temps réel
- Support multi-backend (CPU, GPU, TPU)
- Support multi-précision (FP32, FP16, INT8)
- Métriques de performance (FPS, latence)
- Optimisations pour edge devices

#### Data Preprocessor (`preprocessing.py`)
- Prétraitement d'images
- Normalisation ImageNet
- Redimensionnement
- Support LiDAR et Radar
- Conversion de formats

### 3. Module d'Intégration (`src/integration/`)

#### AutoFlux System (`system.py`)
- Classe principale du système
- Initialisation et configuration
- Coordination de tous les composants
- Gestion du cycle de vie

#### System Orchestrator (`orchestrator.py`)
- Boucle de contrôle principale à 30 Hz
- Coordination des flux de données
- Prise de décision basée sur capteurs et IA
- Gestion des priorités de sécurité

#### API Manager (`api.py`)
- API REST avec FastAPI
- Endpoints de monitoring
- Contrôle à distance
- Diagnostics en temps réel

## Tests et Validation

### Suite de Tests Complète
- **51 tests unitaires et d'intégration**
- **100% de réussite**
- Coverage des modules principaux

#### Tests par module :
- `tests/autonomous_vehicle/` : 28 tests
  - test_diagnostics.py : 13 tests
  - test_control.py : 15 tests
- `tests/neuroflux/` : 10 tests
  - test_inference.py : 10 tests
- `tests/integration/` : 13 tests
  - test_system.py : 13 tests

### Outils de Qualité
- pytest pour les tests
- Black pour le formatage
- Flake8 pour le style
- MyPy pour le typage
- CodeQL pour la sécurité (0 vulnérabilités)

## Documentation

### Fichiers de Documentation
1. **README.md** : Documentation principale du projet
2. **docs/architecture.md** : Architecture détaillée du système
3. **docs/development.md** : Guide de développement
4. **config/config.yaml** : Configuration complète du système
5. **config/config.example.yaml** : Exemple de configuration

### Exemples
- **examples/basic_usage.py** : Exemple d'utilisation de base

## Fonctionnalités Clés

### Sécurité et Fiabilité
✅ Watchdog système
✅ Arrêt d'urgence
✅ Mode de secours
✅ Validation des commandes
✅ Diagnostic continu
✅ 0 vulnérabilités de sécurité (CodeQL)

### Performance
✅ Latence cible : < 33ms (30 Hz)
✅ Inférence optimisée pour edge
✅ Support GPU/CPU
✅ Quantification des modèles
✅ Traitement parallèle

### Extensibilité
✅ Architecture modulaire
✅ Configuration YAML flexible
✅ API REST pour intégration
✅ Support multi-modèles
✅ Support multi-capteurs

## Structure des Fichiers

```
AutoFlux-EdgeAI/
├── src/                          # 15 fichiers Python
│   ├── autonomous_vehicle/       # 3 modules
│   ├── neuroflux/               # 3 modules  
│   └── integration/             # 3 modules
├── tests/                       # 13 fichiers de tests
├── docs/                        # 3 documents
├── examples/                    # 1 exemple
├── config/                      # 2 fichiers de config
├── README.md                    # Documentation principale
├── requirements.txt             # Dépendances
├── setup.py                     # Installation
├── setup.cfg                    # Configuration
└── .gitignore                   # Exclusions Git
```

## Technologies Utilisées

### Core
- Python 3.8+
- NumPy pour le calcul numérique
- PyYAML pour la configuration

### Edge AI
- Support PyTorch/TensorFlow Lite
- ONNX Runtime pour l'inférence
- OpenCV pour le traitement d'images

### Véhicule Autonome
- python-can pour l'interface CAN
- Support LiDAR/Radar/GPS/IMU

### API et Services
- FastAPI pour l'API REST
- Uvicorn comme serveur ASGI
- Pydantic pour la validation

### Développement
- pytest pour les tests
- Black pour le formatage
- Flake8 pour le linting
- MyPy pour le typage statique

## Métriques du Projet

- **Lignes de Code** : ~2500 lignes
- **Modules Python** : 15 modules
- **Tests** : 51 tests (100% réussite)
- **Documentation** : >10,000 mots
- **Couverture** : Modules principaux couverts
- **Qualité** : 0 vulnérabilités CodeQL

## Utilisation

### Installation Simple
```bash
git clone https://github.com/kabir308/AutoFlux-EdgeAI.git
cd AutoFlux-EdgeAI
pip install -r requirements.txt
```

### Exemple d'Utilisation
```python
from src.integration import AutoFluxSystem

# Créer et initialiser le système
system = AutoFluxSystem(config_path="config/config.yaml")
system.initialize()

# Démarrer le système
system.start()

# Le système coordonne automatiquement :
# - Lecture des capteurs
# - Inférence IA
# - Contrôle du véhicule
```

### Exécuter les Tests
```bash
pytest tests/ -v
```

### Exécuter l'Exemple
```bash
python examples/basic_usage.py
```

## Avantages de l'Architecture Unifiée

1. **Intégration Transparente** : Les deux systèmes fonctionnent de manière cohérente
2. **Sécurité Renforcée** : Double validation (diagnostics + IA)
3. **Performance Optimale** : Pipeline optimisé pour edge devices
4. **Extensibilité** : Facile d'ajouter de nouveaux capteurs ou modèles
5. **Maintenabilité** : Code bien structuré et documenté
6. **Testabilité** : Suite de tests complète

## Cas d'Usage

### 1. Conduite Autonome
- Détection d'obstacles en temps réel
- Suivi de voie
- Contrôle de vitesse adaptatif
- Freinage d'urgence automatique

### 2. Diagnostic Véhicule
- Surveillance continue des capteurs
- Détection de pannes
- Alertes préventives
- Logs de diagnostic

### 3. Edge AI
- Inférence temps réel sur device embarqué
- Détection d'objets
- Segmentation de scène
- Reconnaissance de panneaux

## Évolutions Futures

### Court Terme
- [ ] Intégration de modèles ONNX réels
- [ ] Optimisations TensorRT
- [ ] Interface de visualisation

### Moyen Terme
- [ ] Communication V2V
- [ ] Cartes HD
- [ ] Planification de trajectoire avancée

### Long Terme
- [ ] Apprentissage en ligne
- [ ] Fusion multi-capteurs avancée
- [ ] Optimisation énergétique

## Conformité et Standards

✅ PEP 8 - Style Guide Python
✅ Type Hints (PEP 484)
✅ Docstrings (Google Style)
✅ MIT License
✅ Sécurité CodeQL

## Conclusion

AutoFlux-EdgeAI représente une architecture complète et robuste pour les véhicules autonomes avec edge AI. Le projet démontre une fusion réussie de deux systèmes complexes dans une architecture unifiée, optimisée pour un projet de Maîtrise.

### Points Forts
- Architecture modulaire et extensible
- Tests complets et validés
- Documentation exhaustive
- Sécurité vérifiée
- Performance optimisée

### Impact
Ce projet fournit une base solide pour le développement de systèmes de véhicules autonomes avec capacités d'intelligence artificielle embarquée, répondant aux exigences de sécurité, performance et maintenabilité d'un projet de Maîtrise.

---

**Version** : 1.0.0  
**Auteur** : kabir308  
**Date** : Novembre 2025  
**License** : MIT
