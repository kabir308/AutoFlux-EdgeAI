# Documentation AutoFlux-EdgeAI

Cette documentation est déployée automatiquement sur GitHub Pages.

## Fichiers

- `index.md` - Page d'accueil
- `getting-started.md` - Guide de démarrage
- `architecture.md` - Architecture détaillée
- `api.md` - Documentation API
- `packages.md` - Packages et dépendances
- `development.md` - Guide de développement

## Configuration Jekyll

Le site utilise le thème Cayman configuré dans `_config.yml`.

## Déploiement

Le déploiement est automatique via GitHub Actions (`.github/workflows/pages.yml`) lors de chaque push sur la branche principale.

## Visualisation Locale

Pour prévisualiser localement :

```bash
# Installer Jekyll
gem install bundler jekyll

# Créer Gemfile
bundle init
bundle add jekyll

# Lancer le serveur
bundle exec jekyll serve --source docs
```

Ouvrir http://localhost:4000
