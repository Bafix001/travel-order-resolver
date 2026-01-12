# Data Directory

⚠️ Les fichiers de données ne sont pas versionnés (trop gros pour Git).

## Fichiers nécessaires

Placer dans `raw/`:
- `ner.csv` (150MB) - Dataset principal pour NER
- `ner_dataset.csv` (15MB) - Dataset secondaire

## Obtenir les données
[À compléter : lien Google Drive, instructions de téléchargement]

## Structure
```
data/
├── raw/              # Données brutes (CSV non versionnés)
├── processed/        # Données nettoyées (PKL non versionnés)
└── README.md
```
