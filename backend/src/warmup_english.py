import pandas as pd
import spacy
from sklearn.metrics import classification_report


class config:
    # Chemins des données
    RAW_DATA = "../data/raw/ner_dataset.csv"
    ENCODING = "ISO-8859-1"

    # Paramètres du modèle
    MODEL_NAME = "en_core_web_sm"

    # Mapping des entités (pour aligner spaCy avec ton dataset)
    # On transforme les labels spaCy vers les labels simplifiés du dataset
    LABEL_MAPPING = {
        "GPE": "geo", 
        "LOC": "geo", 
        "PERSON": "per", 
        "NORP": "gpe", 
        "DATE": "tim",
        "ORG": "org"
    }
    
    # Phrase de test par défaut
    TEST_SENTENCE_ID = "Sentence: 1"


df = pd.read_csv(config.RAW_DATA, encoding=config.ENCODING, on_bad_lines='skip',engine="python")
print("--- AVANT NETTOYAGE (Brut) ---")
print(df.head(10))
print("-" * 30)

df["Sentence #"] = df["Sentence #"].ffill()

df = df.dropna(subset=["Word"]).copy()
df["Word"] = df["Word"].astype(str)

df["Tag"] = df["Tag"].str.split('-').str[-1]

print("--- APRÈS NETTOYAGE (Tags simplifiés et Sentence # remplis) ---")
print(df.head(10))
print("-" * 30)

print("Aperçu des tags simplifiés :")
print(df["Tag"].unique())

df.describe()
print(df.describe(include='all'))

df.isnull().sum()
print("Vérification des valeurs manquantes :")
print(df.isnull().sum())


# --- ÉTAPE : GROUPEMENT PAR PHRASE ---

nlp = spacy.load(config.MODEL_NAME)

agg_func = lambda s: [
    (w, p, t) for w, p, t in zip(
        s["Word"].values.tolist(),
        s["POS"].values.tolist(),
        s["Tag"].values.tolist()
    )
]

# Groupement
sentences_grouped = df.groupby("Sentence #").apply(agg_func)

phrase_data = sentences_grouped[config.TEST_SENTENCE_ID]

words = [w for w, p, t in phrase_data]
full_text = " ".join(words)

y_true = [t for w, p, t in phrase_data]

doc = nlp(full_text)

# --- ÉTAPE : ALIGNEMENT ET MAPPING ---

y_pred = []

for token in doc:
    label_spacy = token.ent_type_
    label_final = config.LABEL_MAPPING.get(label_spacy, "O")
    y_pred.append(label_final)

# --- ÉTAPE : AFFICHAGE COMPARATIF ET SCORE ---

min_len = min(len(y_true), len(y_pred))
print(f"\n--- COMPARAISON SUR {config.TEST_SENTENCE_ID} ---")
print(f"{'MOT':<15} | {'VÉRITÉ':<10} | {'PRÉDICTION':<10}")
print("-" * 40)

for i in range(min_len):
    print(f"{words[i]:<15} | {y_true[i]:<10} | {y_pred[i]:<10}")

print("\n--- RAPPORT DE CLASSIFICATION (SKLEARN) ---")
print(classification_report(y_true[:min_len], y_pred[:min_len], zero_division=0))

