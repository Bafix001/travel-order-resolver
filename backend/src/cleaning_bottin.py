import pandas as pd
import re
import html
import os

class config:
    # 1. Chemins des données
    RAW_DATA = "../data/raw/bottins.csv"
    PROCESSED_DATA_DIR = "../data/processed"
    OUTPUT_FILE = "../data/processed/bottin_cleaned.pkl"
    
    # 2. Paramètres du modèle
    MODEL_NAME = "fr_core_news_sm"
    
    # 3. Paramètres de lecture
    COLUMN_NAMES = ["raw_text", "source"]

def clean_xml_text(text):
    """
    Nettoie les scories HTML et harmonise le texte.
    - unescape: transforme &apos; en '
    - replace: supprime les sauts de ligne
    - sub: réduit les espaces multiples
    """
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_bio_entities(text):
    """
    Transforme un texte balisé XML en liste de tuples (Mot, Tag_BIO).
    Gère les entités multi-mots (B- et I-) et ignore les tokens vides.
    """
    # Regex pour capturer <TAG>Contenu</TAG>
    tag_pattern = r'<(\w+)>(.*?)</\1>'
    
    # Découpage du texte en conservant les balises
    parts = re.split(tag_pattern, text)
    entities = []
    
    i = 0
    while i < len(parts):
        # 1. Traitement du texte Hors-Balise (Tag 'O')
        outside_text = parts[i].strip()
        if outside_text:
            for word in outside_text.split():
                clean_word = word.strip(',').strip()
                if clean_word:
                    entities.append((clean_word, 'O'))
        
        # 2. Traitement du texte Dans-Balise (Tags B- et I-)
        if i + 2 < len(parts):
            tag_name = parts[i+1]
            content = parts[i+2].strip()
            words = content.split()
            
            for j, word in enumerate(words):
                prefix = "B-" if j == 0 else "I-"
                clean_word = word.strip()
                if clean_word:
                    entities.append((clean_word, f"{prefix}{tag_name}"))
        i += 3
        
    return entities

# --- EXECUTION DU SCRIPT ---

if __name__ == "__main__":
    print("Démarrage du nettoyage du Bottin...")

    try:
        # Chargement des données
        df = pd.read_csv(
            config.RAW_DATA, 
            sep=',', 
            names=config.COLUMN_NAMES, 
            engine='python'
        )
        
        # Étape 1 : Nettoyage du texte brut
        df["clean_text"] = df["raw_text"].apply(clean_xml_text)
        
        # Étape 2 : Extraction BIO (La vérité terrain)
        print("Extraction des entités BIO...")
        df["entities"] = df["clean_text"].apply(get_bio_entities)
        
        # Étape 3 : Création de la phrase 'nue' pour l'IA
        df["final_sentence"] = df["clean_text"].apply(lambda x: re.sub(r'<.*?>', '', x))
        
        # --- VERIFICATION VISUELLE ---
        print("\n--- TEST SUR LA LIGNE 0 ---")
        test_res = df["entities"].iloc[0]
        for word, tag in test_res:
            print(f"{word:<20} -> {tag}")
            
        # --- SAUVEGARDE ---
        os.makedirs(config.PROCESSED_DATA_DIR, exist_ok=True)
        df.to_pickle(config.OUTPUT_FILE)
        
        print(f"\nSuccès ! {len(df)} lignes traitées.")
        print(f"Fichier sauvegardé ici : {config.OUTPUT_FILE}")

    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")