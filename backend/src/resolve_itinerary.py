import torch
import json
import os
from transformers import AutoTokenizer, AutoModelForTokenClassification
from graph_optimizer import build_delivery_graph, solve_tsp 

# --- Ta fonction extract_locations (NER) ---
def extract_locations(text, model, tokenizer, id2tag):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=64)
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    
    locations = []
    current_loc = ""
    for token, pred_id in zip(tokens, predictions[0].tolist()):
        tag = id2tag[pred_id]
        if token in ["<s>", "</s>", "<pad>"]: continue
        clean_token = token.replace(" ", " ").replace("▁", "")
        if "LOC" in tag:
            if token.startswith(" ") or token.startswith("▁") or not current_loc:
                current_loc += " " + clean_token
            else:
                current_loc += clean_token
        else:
            if current_loc:
                locations.append(current_loc.strip())
                current_loc = ""
    return locations

def run_full_resolver(commandes, model, tokenizer, id2tag):
    extracted_data = []
    unique_locs = []
    for cmd in commandes:
        found_locs = extract_locations(cmd, model, tokenizer, id2tag)
        if found_locs:
            loc = found_locs[0].strip(" ,")
            if len(loc) > 2:
                if loc not in unique_locs: unique_locs.append(loc)

    if not unique_locs: return []

    G, pos = build_delivery_graph(unique_locs)
    itineraire_ordonne = solve_tsp(G)
    
    # Formatage pour Refine v4
    feuille_de_route = []
    for rang, etape in enumerate(itineraire_ordonne):
        feuille_de_route.append({
            "id": rang + 1,
            "adresse": etape,
            "type": "Livraison" if etape != "DEPOT" else "Base",
            "ordre_passage": rang
        })
    return feuille_de_route

if __name__ == "__main__":
    path = "../models/camembert_bottin"
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForTokenClassification.from_pretrained(path)
    id2tag = {0: 'B-ACT', 1: 'B-CARDINAL', 2: 'B-FT', 3: 'B-LOC', 4: 'B-PER', 
              5: 'B-TITRE', 6: 'I-ACT', 7: 'I-FT', 8: 'I-LOC', 9: 'I-PER', 10: 'I-TITRE', 11: 'O'}

    commandes_du_jour = [
        "Dufay, papetier, r. d'Anjou, 10",
        "Clémendot, pharmacien, r. de la Harpe, 45",
        "Dulay, chaudronnier, r. Saint-Honoré, 122"
    ]

    resultat = run_full_resolver(commandes_du_jour, model, tokenizer, id2tag)
    
    # SAUVEGARDE DIRECTE DANS LE FRONTEND
    # Ajuste le chemin si ton dossier frontend s'appelle autrement
    target_path = "../frontend/public/data.json"
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(resultat, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fichier JSON créé dans {target_path}")