---
layout: default
title: API Documentation
---

# 📡 API Documentation

## Vue d'ensemble de l'API

AutoFlux-EdgeAI expose une API REST complète pour le monitoring, le contrôle et la configuration du système.

---

## 🔌 Endpoint Base

```
http://localhost:8000
```

Configuration par défaut. Modifiable dans `config/config.yaml`.

---

## 🚀 Endpoints Principaux

### GET / - Root

**Description** : Informations de base sur le système

**Response**:
```json
{
  "name": "AutoFlux-EdgeAI",
  "version": "1.0.0",
  "status": "running"
}
```

---

### GET /status - System Status

**Description** : État complet du système

**Response**:
```json
{
  "running": true,
  "sensors": {
    "lidar": {
      "type": "lidar",
      "status": "initialized",
      "last_update": "2025-11-02T10:00:00",
      "data_available": true
    },
    "camera_0": { /* ... */ },
    "radar": { /* ... */ },
    "gps": { /* ... */ },
    "imu": { /* ... */ }
  },
  "diagnostics": {
    "status": "healthy",
    "message": "All systems operational",
    "critical_count": 0,
    "error_count": 0,
    "warning_count": 0
  },
  "control": {
    "mode": "assisted",
    "emergency_stop": false,
    "current_command": {
      "steering": 0.0,
      "throttle": 0.0,
      "brake": 0.0
    },
    "vehicle_state": {
      "speed_mps": 15.0,
      "steering_angle": 0.0
    }
  },
  "models": {
    "object_detection": {
      "type": "object_detection",
      "loaded": true,
      "simulation_mode": false,
      "path": "models/yolov8n.onnx",
      "input_size": [640, 640],
      "confidence_threshold": 0.5
    },
    /* ... autres modèles ... */
  },
  "inference": {
    "total_inferences": 1250,
    "total_time_ms": 41500.0,
    "average_time_ms": 33.2,
    "fps": 30.1,
    "accelerator": "gpu",
    "precision": "fp16"
  }
}
```

---

### GET /health - Health Check

**Description** : Vérification rapide de santé

**Response**:
```json
{
  "status": "healthy"
}
```

**Status Codes**:
- `200 OK` : Système en bonne santé
- `503 Service Unavailable` : Système non opérationnel

---

### POST /emergency-stop - Emergency Stop

**Description** : Déclenche l'arrêt d'urgence

**Request**: Aucun body requis

**Response**:
```json
{
  "status": "emergency_stop_activated"
}
```

**Effet** : 
- Arrêt immédiat du véhicule
- Freinage maximal
- Blocage des commandes de mouvement

---

### GET /sensors - Sensor Status

**Description** : État détaillé de tous les capteurs

**Response**:
```json
{
  "lidar": {
    "type": "lidar",
    "status": "initialized",
    "last_update": "2025-11-02T10:00:00.000Z",
    "data_available": true,
    "config": {
      "update_rate_hz": 10,
      "max_range_m": 200,
      "num_channels": 64
    }
  },
  "camera_0": {
    "type": "camera",
    "status": "initialized",
    "last_update": "2025-11-02T10:00:00.033Z",
    "data_available": true,
    "config": {
      "resolution": [1920, 1080],
      "fps": 30
    }
  }
  /* ... autres capteurs ... */
}
```

---

### GET /diagnostics - Diagnostic Summary

**Description** : Résumé des diagnostics système

**Response**:
```json
{
  "status": "healthy",
  "message": "All systems operational",
  "critical_count": 0,
  "error_count": 0,
  "warning_count": 0,
  "recent_reports": [
    {
      "timestamp": "2025-11-02T10:00:00",
      "component": "sensors",
      "level": "info",
      "message": "All sensors operating normally"
    }
  ]
}
```

**Status Values**:
- `healthy` : Tous les systèmes fonctionnent normalement
- `warning` : Avertissements présents
- `error` : Erreurs détectées
- `critical` : Problèmes critiques nécessitant attention

---

### GET /models - Models Information

**Description** : Informations sur les modèles AI chargés

**Response**:
```json
{
  "object_detection": {
    "type": "object_detection",
    "loaded": true,
    "simulation_mode": false,
    "path": "models/yolov8n.onnx",
    "input_size": [640, 640],
    "confidence_threshold": 0.5
  },
  "semantic_segmentation": {
    "type": "semantic_segmentation",
    "loaded": true,
    "simulation_mode": false,
    "path": "models/deeplabv3.onnx",
    "num_classes": 20,
    "input_size": [512, 512]
  },
  "lane_detection": {
    "type": "lane_detection",
    "loaded": true,
    "simulation_mode": false,
    "path": "models/ufld.onnx",
    "input_size": [800, 288]
  }
}
```

---

### GET /performance - Performance Statistics

**Description** : Statistiques de performance d'inférence

**Response**:
```json
{
  "total_inferences": 1250,
  "total_time_ms": 41500.0,
  "average_time_ms": 33.2,
  "fps": 30.1,
  "accelerator": "gpu",
  "precision": "fp16",
  "batch_size": 1
}
```

---

## 🔒 Sécurité

### Authentication (Future)

L'API ne requiert actuellement pas d'authentification. Pour un déploiement en production, il est recommandé d'ajouter :

- Bearer Token Authentication
- API Keys
- Rate Limiting
- HTTPS/TLS

---

## 🌐 CORS Configuration

Par défaut, CORS est configuré pour accepter les requêtes de :
- `localhost`
- `127.0.0.1`

Configuration dans `config/config.yaml` :

```yaml
integration:
  api:
    cors_origins:
      - "http://localhost:3000"
      - "https://yourdomain.com"
```

---

## 📊 Monitoring en Temps Réel

### WebSocket Support (Future)

Pour le monitoring en temps réel, utilisez les WebSockets :

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('System status:', data);
};
```

---

## 🔧 Configuration de l'API

### Dans config.yaml

```yaml
integration:
  api:
    enabled: true
    host: "0.0.0.0"
    port: 8000
    workers: 4
    reload: false  # Dev only
    log_level: "info"
```

---

## 💡 Exemples d'Utilisation

### Python

```python
import requests

# Obtenir le status
response = requests.get('http://localhost:8000/status')
status = response.json()
print(f"System running: {status['running']}")

# Arrêt d'urgence
response = requests.post('http://localhost:8000/emergency-stop')
print(response.json())
```

### JavaScript

```javascript
// Fetch status
fetch('http://localhost:8000/status')
  .then(response => response.json())
  .then(data => {
    console.log('System status:', data);
  });

// Emergency stop
fetch('http://localhost:8000/emergency-stop', {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => {
    console.log('Emergency stop:', data);
  });
```

### cURL

```bash
# Get status
curl http://localhost:8000/status

# Health check
curl http://localhost:8000/health

# Emergency stop
curl -X POST http://localhost:8000/emergency-stop

# Get sensors
curl http://localhost:8000/sensors
```

---

## 📝 Response Codes

| Code | Signification | Description |
|------|---------------|-------------|
| 200 | OK | Requête réussie |
| 400 | Bad Request | Requête invalide |
| 404 | Not Found | Endpoint introuvable |
| 500 | Internal Server Error | Erreur serveur |
| 503 | Service Unavailable | Service non disponible |

---

## 🚧 Endpoints Futurs

### POST /control/command
Envoyer des commandes de contrôle

### GET /logs
Accéder aux logs système

### POST /config
Mettre à jour la configuration

### GET /metrics
Métriques Prometheus

---

## 📚 Ressources Additionnelles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification](http://localhost:8000/docs) - Swagger UI
- [ReDoc](http://localhost:8000/redoc) - Alternative documentation
