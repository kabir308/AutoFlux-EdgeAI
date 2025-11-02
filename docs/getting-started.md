---
layout: default
title: Getting Started
---

# 🚀 Guide de Démarrage

Bienvenue dans AutoFlux-EdgeAI ! Ce guide vous aidera à installer et démarrer avec le système.

---

## ⚡ Installation Rapide

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- 4 GB RAM minimum
- (Optionnel) GPU NVIDIA avec CUDA pour accélération

### Installation en 3 Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/kabir308/AutoFlux-EdgeAI.git
cd AutoFlux-EdgeAI

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer
cp config/config.example.yaml config/config.yaml
```

---

## 🎯 Premier Exemple

### Exemple de Base

Créez un fichier `quick_start.py` :

```python
from src.integration import AutoFluxSystem

# Créer le système
system = AutoFluxSystem(config_path="config/config.yaml")

# Initialiser
system.initialize()

# Démarrer
system.start()

# Obtenir le status
status = system.get_system_status()
print(f"Système en marche: {status['running']}")
print(f"Capteurs: {len(status['sensors'])}")
print(f"Modèles: {len(status['models'])}")

# Arrêter
system.stop()
```

Exécuter :

```bash
python quick_start.py
```

---

## 📝 Configuration de Base

### Fichier config.yaml

Le fichier de configuration contrôle tous les aspects du système :

```yaml
autonomous_vehicle:
  sensors:
    lidar:
      enabled: true
      update_rate_hz: 10
    camera:
      enabled: true
      num_cameras: 4
      fps: 30
    
  control:
    mode: assisted  # manual, assisted, autonomous
    max_speed_mps: 20.0

neuroflux:
  hardware:
    accelerator: cpu  # cpu, gpu, tpu
    precision: fp32   # fp32, fp16, int8
  
  models:
    object_detection:
      model_name: yolov8n
      confidence_threshold: 0.5

integration:
  system:
    update_rate_hz: 30
  api:
    enabled: true
    port: 8000
```

---

## 🧪 Exécuter les Tests

Vérifier que tout fonctionne :

```bash
# Installer pytest si nécessaire
pip install pytest

# Exécuter tous les tests
pytest tests/ -v

# Tests spécifiques
pytest tests/autonomous_vehicle/
pytest tests/neuroflux/
pytest tests/integration/
```

Résultat attendu :
```
51 passed in 0.24s
```

---

## 🎮 Modes de Contrôle

### Mode Manual

Le véhicule est contrôlé manuellement.

```yaml
autonomous_vehicle:
  control:
    mode: manual
```

### Mode Assisted

Le système assiste le conducteur avec :
- Freinage d'urgence automatique
- Avertissements de collision
- Maintien de voie

```yaml
autonomous_vehicle:
  control:
    mode: assisted
```

### Mode Autonomous

Conduite entièrement autonome.

```yaml
autonomous_vehicle:
  control:
    mode: autonomous
```

---

## 🔍 Monitoring avec l'API

### Démarrer l'API

L'API démarre automatiquement avec le système :

```python
system = AutoFluxSystem()
system.initialize()
system.start()
# API disponible sur http://localhost:8000
```

### Vérifier le Status

```bash
# Status complet
curl http://localhost:8000/status

# Health check
curl http://localhost:8000/health

# Capteurs
curl http://localhost:8000/sensors

# Performance
curl http://localhost:8000/performance
```

---

## 🎨 Interface Web (Future)

Un dashboard web sera disponible sur :
```
http://localhost:8000/dashboard
```

Fonctionnalités :
- Monitoring en temps réel
- Visualisation des capteurs
- Contrôles du véhicule
- Métriques de performance

---

## 📦 Charger des Modèles

### Ajouter vos Modèles ONNX

1. Placer les modèles dans `models/` :
```
models/
├── yolov8n.onnx
├── deeplabv3.onnx
└── ufld.onnx
```

2. Configurer dans `config.yaml` :
```yaml
neuroflux:
  models:
    object_detection:
      model_path: models/yolov8n.onnx
      input_size: [640, 640]
```

3. Le système charge automatiquement les modèles au démarrage.

---

## 🐛 Debugging

### Activer les Logs Détaillés

```yaml
integration:
  monitoring:
    log_level: DEBUG
```

### Logs en Console

```python
import logging
logging.basicConfig(level=logging.DEBUG)

system = AutoFluxSystem()
system.initialize()
```

---

## 🚨 Arrêt d'Urgence

### Via Code

```python
system.emergency_stop()
```

### Via API

```bash
curl -X POST http://localhost:8000/emergency-stop
```

---

## 📊 Exemples Avancés

### Traitement d'une Frame Caméra

```python
import numpy as np

# Lire une image
image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

# Inférence
result = system.inference_engine.run_object_detection(image)

# Résultats
for detection in result.predictions:
    print(f"Objet: {detection['class']}, Confiance: {detection['confidence']}")
```

### Contrôle Manuel

```python
from src.autonomous_vehicle.control import ControlCommand
import time

command = ControlCommand(
    steering_angle=10.0,  # degrés
    throttle=0.3,         # 0-1
    brake=0.0,            # 0-1
    timestamp=time.time()
)

system.vehicle_controller.execute_command(command)
```

---

## 🔧 Troubleshooting

### Problème : Modèles non trouvés

**Solution** : Les modèles s'exécutent en mode simulation par défaut.

```
WARNING - Model file not found: models/yolov8n.onnx. 
         Model object_detection will run in simulation mode.
```

Pour utiliser de vrais modèles, placez les fichiers ONNX dans `models/`.

### Problème : Port API déjà utilisé

**Solution** : Changer le port dans `config.yaml` :

```yaml
integration:
  api:
    port: 8001
```

### Problème : Erreur d'importation

**Solution** : Réinstaller les dépendances :

```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Prochaines Étapes

1. **[Architecture](architecture.html)** - Comprendre l'architecture du système
2. **[API Documentation](api.html)** - Utiliser l'API REST
3. **[Development Guide](development.html)** - Contribuer au projet
4. **[Packages](packages.html)** - Explorer les dépendances

---

## 💬 Support

- **Issues** : [GitHub Issues](https://github.com/kabir308/AutoFlux-EdgeAI/issues)
- **Documentation** : [https://kabir308.github.io/AutoFlux-EdgeAI/](https://kabir308.github.io/AutoFlux-EdgeAI/)
- **Examples** : Voir `examples/basic_usage.py`

---

## ✅ Checklist de Démarrage

- [ ] Python 3.8+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Configuration créée (`config/config.yaml`)
- [ ] Tests passent (`pytest tests/`)
- [ ] Exemple de base fonctionne
- [ ] API accessible (`http://localhost:8000`)

Félicitations ! Vous êtes prêt à utiliser AutoFlux-EdgeAI ! 🎉
