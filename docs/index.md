---
layout: default
title: AutoFlux-EdgeAI
---

# AutoFlux-EdgeAI

<div class="hero-section">
  <h2>🚗 Architecture Unifiée pour Véhicule Autonome et Edge AI</h2>
  <p class="lead">
    Une solution innovante fusionnant <strong>VOITURE-AUTONOME-ET-DIAGNOSTIC-</strong> et <strong>NeuroFlux</strong> 
    dans une architecture optimisée pour l'intelligence artificielle embarquée.
  </p>
</div>

---

## 🎯 Vue d'Ensemble

AutoFlux-EdgeAI combine les capacités de diagnostic et de contrôle de véhicules autonomes avec l'intelligence artificielle embarquée (Edge AI) pour créer un système intelligent de gestion et de prise de décision en temps réel.

### Caractéristiques Principales

<div class="features-grid">
  <div class="feature">
    <h3>🔍 Diagnostic Intelligent</h3>
    <p>Surveillance en temps réel des capteurs et systèmes avec 4 niveaux de sévérité</p>
  </div>
  
  <div class="feature">
    <h3>🚦 Contrôle Autonome</h3>
    <p>3 modes de conduite avec contraintes de sécurité et freinage d'urgence</p>
  </div>
  
  <div class="feature">
    <h3>🧠 Edge AI</h3>
    <p>Inférence en temps réel sur GPU/CPU avec modèles ONNX optimisés</p>
  </div>
  
  <div class="feature">
    <h3>📡 Multi-Capteurs</h3>
    <p>Support LiDAR, 4 caméras, radar, GPS et IMU</p>
  </div>
</div>

---

## 📦 Installation

### Prérequis

- Python 3.8+
- pip
- (Optionnel) GPU CUDA pour accélération

### Installation Rapide

```bash
# Cloner le dépôt
git clone https://github.com/kabir308/AutoFlux-EdgeAI.git
cd AutoFlux-EdgeAI

# Installer les dépendances
pip install -r requirements.txt

# Configurer
cp config/config.example.yaml config/config.yaml
```

### Installation avec Package

```bash
pip install -e .
```

---

## 🚀 Démarrage Rapide

```python
from src.integration import AutoFluxSystem

# Créer le système
system = AutoFluxSystem(config_path="config/config.yaml")

# Initialiser
system.initialize()

# Démarrer
system.start()

# Le système coordonne automatiquement :
# - Lecture des capteurs
# - Inférence des modèles NeuroFlux
# - Décisions de contrôle du véhicule
```

---

## 🏗️ Architecture

<div class="architecture-diagram">
  <pre>
┌─────────────────────────────────────────────────────────┐
│               AutoFlux-EdgeAI System                     │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────┐      ┌──────────────────┐        │
│  │  Autonomous      │      │    NeuroFlux     │        │
│  │  Vehicle Module  │◄────►│  Edge AI Module  │        │
│  └──────────────────┘      └──────────────────┘        │
│           │                         │                    │
│           └────────┬────────────────┘                    │
│                    │                                     │
│           ┌────────▼────────┐                           │
│           │   Integration   │                           │
│           │     Module      │                           │
│           └─────────────────┘                           │
└─────────────────────────────────────────────────────────┘
  </pre>
</div>

### Modules

- **[Module Véhicule Autonome](architecture.html#autonomous-vehicle)** : Diagnostic, contrôle, capteurs
- **[Module NeuroFlux](architecture.html#neuroflux)** : Modèles AI, inférence, préprocessing
- **[Module d'Intégration](architecture.html#integration)** : Orchestration, API, gestion de données

[→ Voir l'architecture détaillée](architecture.html)

---

## 📊 Statistiques

<div class="stats-grid">
  <div class="stat">
    <div class="stat-number">51</div>
    <div class="stat-label">Tests</div>
    <div class="stat-value">100% Pass</div>
  </div>
  
  <div class="stat">
    <div class="stat-number">15</div>
    <div class="stat-label">Modules Python</div>
    <div class="stat-value">~2500 LOC</div>
  </div>
  
  <div class="stat">
    <div class="stat-number">0</div>
    <div class="stat-label">Vulnérabilités</div>
    <div class="stat-value">CodeQL</div>
  </div>
  
  <div class="stat">
    <div class="stat-number">30Hz</div>
    <div class="stat-label">Fréquence</div>
    <div class="stat-value">Control Loop</div>
  </div>
</div>

---

## 📚 Documentation

- **[Guide de Démarrage](getting-started.html)** - Installation et premiers pas
- **[Architecture](architecture.html)** - Architecture détaillée du système
- **[Guide API](api.html)** - Documentation de l'API REST
- **[Guide Développeur](development.html)** - Contribution et développement
- **[Packages](packages.html)** - Information sur les packages et dépendances

---

## 🎓 Projet de Maîtrise

Ce projet a été développé dans le cadre d'un projet de Maîtrise en Ingénierie, démontrant :

- ✅ Architecture logicielle avancée
- ✅ Intégration de systèmes complexes
- ✅ Edge AI et optimisations
- ✅ Sécurité et fiabilité
- ✅ Documentation académique complète

---

## 📄 License

MIT License - voir [LICENSE](https://github.com/kabir308/AutoFlux-EdgeAI/blob/main/LICENSE)

---

## 🔗 Liens Rapides

- [GitHub Repository](https://github.com/kabir308/AutoFlux-EdgeAI)
- [Issues](https://github.com/kabir308/AutoFlux-EdgeAI/issues)
- [Pull Requests](https://github.com/kabir308/AutoFlux-EdgeAI/pulls)

<style>
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.lead {
  font-size: 1.2rem;
  margin: 1rem 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.feature {
  border: 1px solid #e1e4e8;
  padding: 1.5rem;
  border-radius: 6px;
  background: #f6f8fa;
}

.feature h3 {
  margin-top: 0;
  color: #0366d6;
}

.architecture-diagram {
  background: #f6f8fa;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.stat {
  text-align: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-top: 0.5rem;
}

.stat-value {
  font-size: 0.85rem;
  opacity: 0.8;
  margin-top: 0.25rem;
}
</style>
