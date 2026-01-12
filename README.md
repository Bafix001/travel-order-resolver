# Travel Order Resolver

🚚 Système intelligent de résolution d'itinéraires de livraison utilisant NER et optimisation de graphe.

## Architecture
```
travel-order-resolver/
├── backend/          # Pipeline IA (NER + optimisation)
│   ├── data/         # Datasets (non versionnés)
│   ├── models/       # Modèles entraînés (non versionnés)
│   ├── notebooks/    # Jupyter notebooks
│   └── src/          # Code source Python
└── frontend/         # Interface Refine v4
    └── src/          # Code source React/TypeScript
```

## Backend

**Technologies**: Python, Transformers (CamemBERT), NetworkX, SpaCy

- Extraction d'adresses via NER fine-tuné sur corpus français
- Optimisation d'itinéraire avec algorithme de parcours de graphe
- APIs de prédiction

Voir [backend/README.md](backend/README.md)

## Frontend

**Technologies**: React, TypeScript, Refine v4, Ant Design

- Interface de visualisation des itinéraires optimisés
- Tableau interactif avec ordre de passage
- Intégration temps réel avec le backend

Voir [frontend/README.MD](frontend/README.MD)

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python src/predict_bottin.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Notes

- Les fichiers de données (CSV 150MB+) et modèles (420MB) ne sont pas versionnés
- Voir `backend/data/README.md` et `backend/models/README.md` pour les obtenir
