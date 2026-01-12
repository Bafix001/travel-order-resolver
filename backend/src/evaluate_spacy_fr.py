import pandas as pd
import spacy
from sklearn.metrics import classification_report

class config:
    DATA_PATH = "../data/processed/bottin_cleaned.pkl"
    MODEL_NAME = "fr_core_news_sm"

def simplify_tag(tag):
    if "-" in tag:
        main_tag = tag.split("-")[1].lower()
        if main_tag in ["loc", "per"]:
            return main_tag
    return "O"

# 1. Chargement (maintenant que tu l'as téléchargé)
nlp = spacy.load(config.MODEL_NAME)
df = pd.read_pickle(config.DATA_PATH)

all_y_true = []
all_y_pred = []

print(f"Lancement de l'évaluation sur {len(df)} lignes...")

# On teste sur les 500 premières lignes pour avoir un score représentatif
for index, row in df.head(500).iterrows():
    sentence = row["final_sentence"]
    true_entities = row["entities"]
    
    doc = nlp(sentence)
    y_true = [simplify_tag(tag) for word, tag in true_entities]
    
    # Extraction simplifiée des prédictions
    # On crée une liste de 'O' de la même taille que la vérité terrain
    current_preds = ["O"] * len(y_true)
    
    # SpaCy trouve des entités (ex: de l'index 5 à 7)
    # On essaie de les faire correspondre à nos mots
    for ent in doc.ents:
        label = ent.label_.lower()
        if label in ["loc", "per"]:
            # On marque tous les mots de l'entité trouvée par spaCy
            for i in range(ent.start, ent.end):
                if i < len(current_preds):
                    current_preds[i] = "loc" if label == "loc" else "per"
    
    all_y_true.extend(y_true)
    all_y_pred.extend(current_preds)

print("\n--- RÉSULTATS SPACY (FRANÇAIS) ---")
print(classification_report(all_y_true, all_y_pred, zero_division=0))