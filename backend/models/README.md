# Models Directory

⚠️ Les modèles entraînés ne sont pas versionnés (420MB).

## Entraîner le modèle
```bash
cd backend
python src/train_camembert_ner.py
```

## Structure attendue
```
models/camembert_bottin/
├── config.json
├── tokenizer_config.json
├── model.safetensors (420MB - non versionné)
├── sentencepiece.bpe.model
└── ...
```
