# AutoFlux-EdgeAI

## Architecture Unifiée pour Véhicule Autonome et Edge AI

Ce projet représente la fusion des systèmes **VOITURE-AUTONOME-ET-DIAGNOSTIC-** et **NeuroFlux** dans une architecture unifiée, optimisée pour un projet de Maîtrise.

### 🎯 Objectif

AutoFlux-EdgeAI combine les capacités de diagnostic et de contrôle de véhicules autonomes avec l'intelligence artificielle embarquée (Edge AI) pour créer un système intelligent de gestion et de prise de décision en temps réel.

### 🏗️ Architecture

Le projet est structuré en trois modules principaux :

#### 1. Module Véhicule Autonome (`autonomous_vehicle`)
- **Diagnostic des Capteurs** : Surveillance et validation des données des capteurs (LiDAR, caméras, radar, GPS)
- **Contrôle du Véhicule** : Gestion de la direction, accélération, freinage
- **Interface CAN** : Communication avec le bus CAN du véhicule
- **Gestion des Erreurs** : Détection et correction des défaillances

#### 2. Module NeuroFlux (`neuroflux`)
- **Inférence Edge AI** : Modèles de réseaux neuronaux optimisés pour l'embarqué
- **Traitement d'Images** : Détection d'objets, segmentation, reconnaissance
- **Optimisation Matérielle** : Support pour GPU embarqué, quantification des modèles
- **Pipeline de Données** : Prétraitement et post-traitement optimisés

#### 3. Module d'Intégration (`integration`)
- **API Unifiée** : Interface commune pour les deux systèmes
- **Orchestration** : Coordination des modules et gestion des priorités
- **Cache de Données** : Gestion efficace des données partagées
- **Monitoring** : Surveillance des performances et de la santé du système

### 📁 Structure du Projet

```
AutoFlux-EdgeAI/
├── src/
│   ├── autonomous_vehicle/      # Module de diagnostic et contrôle automobile
│   │   ├── diagnostics/         # Système de diagnostic
│   │   ├── control/             # Contrôle du véhicule
│   │   ├── sensors/             # Gestion des capteurs
│   │   └── can_interface/       # Communication CAN
│   ├── neuroflux/               # Module Edge AI
│   │   ├── models/              # Modèles de réseaux neuronaux
│   │   ├── inference/           # Moteur d'inférence
│   │   ├── preprocessing/       # Prétraitement des données
│   │   └── optimization/        # Optimisations pour edge computing
│   └── integration/             # Intégration des modules
│       ├── api/                 # API unifiée
│       ├── orchestrator/        # Orchestrateur
│       └── data_manager/        # Gestion des données
├── tests/                       # Tests unitaires et d'intégration
├── docs/                        # Documentation
├── config/                      # Fichiers de configuration
└── examples/                    # Exemples d'utilisation

```

### 🚀 Installation

```bash
# Cloner le dépôt
git clone https://github.com/kabir308/AutoFlux-EdgeAI.git
cd AutoFlux-EdgeAI

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp config/config.example.yaml config/config.yaml
```

### 💻 Utilisation

```python
from src.integration import AutoFluxSystem

# Initialiser le système
system = AutoFluxSystem()

# Démarrer le système
system.start()

# Le système coordonne automatiquement :
# - La collecte des données des capteurs
# - L'inférence des modèles NeuroFlux
# - Les décisions de contrôle du véhicule
```

### 🔧 Configuration

Le système peut être configuré via le fichier `config/config.yaml` :

```yaml
autonomous_vehicle:
  sensors:
    lidar: enabled
    camera: enabled
    radar: enabled
  control:
    mode: assisted  # autonomous, assisted, manual

neuroflux:
  models:
    detection: yolov8_optimized
    segmentation: deeplabv3_lite
  hardware:
    accelerator: gpu  # gpu, cpu, tpu
    precision: fp16   # fp32, fp16, int8

integration:
  update_rate_hz: 30
  priority: safety_first
```

### 📊 Fonctionnalités Clés

1. **Diagnostic en Temps Réel** : Surveillance continue de l'état du véhicule
2. **Détection d'Objets** : Identification des obstacles, piétons, véhicules
3. **Prise de Décision Intelligente** : Fusion des données capteurs et IA
4. **Optimisation Edge** : Inférence rapide avec ressources limitées
5. **Sécurité Fonctionnelle** : Systèmes de secours et validation

### 🧪 Tests

```bash
# Exécuter tous les tests
pytest tests/

# Tests spécifiques
pytest tests/autonomous_vehicle/
pytest tests/neuroflux/
pytest tests/integration/
```

### 📚 Documentation

La documentation complète est disponible dans le dossier `docs/` :
- [Architecture Détaillée](docs/architecture.md)
- [Guide API](docs/api.md)
- [Guide de Développement](docs/development.md)
- [Sécurité et Conformité](docs/security.md)

### 🤝 Contribution

Ce projet est développé dans le cadre d'un projet de Maîtrise. Les contributions sont les bienvenues.

### 📄 License

MIT License - voir le fichier [LICENSE](LICENSE)

### 👥 Auteurs

- Développé pour le projet de Maîtrise en Ingénierie
- Intégration VOITURE-AUTONOME-ET-DIAGNOSTIC- et NeuroFlux

### 🔗 Technologies

- Python 3.8+
- PyTorch / TensorFlow Lite
- OpenCV
- NumPy / Pandas
- python-can (Interface CAN)
- FastAPI (API)
