import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification

# 1. Charger le modèle que TU as entraîné
model_path = "../models/camembert_bottin"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

# Ton dictionnaire de tags (doit être le même que pendant l'entraînement)
# Attention : assure-toi que l'ordre correspond à tes "Tags trouvés" de tout à l'heure
id2tag = {0: 'B-ACT', 1: 'B-CARDINAL', 2: 'B-FT', 3: 'B-LOC', 4: 'B-PER', 
          5: 'B-TITRE', 6: 'I-ACT', 7: 'I-FT', 8: 'I-LOC', 9: 'I-PER', 10: 'I-TITRE', 11: 'O'}

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=64)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    predictions = torch.argmax(outputs.logits, dim=2)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    
    # On affiche le résultat
    for token, pred in zip(tokens, predictions[0].tolist()):
        if token not in ["<s>", "</s>", "<pad>"]:
            print(f"{token:<15} -> {id2tag[pred]}")

# Testons une adresse au hasard
predict("Dufay, papetier, r. d'Anjou, 10")