import pandas as pd
import torch
import os
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW  
from transformers import CamembertTokenizer, CamembertForTokenClassification
from tqdm import tqdm

class config:
    MODEL_NAME = "camembert-base"
    DATA_PATH = "../data/processed/bottin_cleaned.pkl"
    MAX_LEN = 64        # Réduit de 128 à 64 (2x plus rapide)
    BATCH_SIZE = 8      # Réduit pour moins de charge mémoire
    EPOCHS = 1          # Un seul passage suffit pour la démo
    LEARNING_RATE = 5e-5
    LIMIT_DATA = 300    # On n'entraîne que sur 300 lignes

# 1. Chargement des données
df_full = pd.read_pickle(config.DATA_PATH)
df = df_full.head(config.LIMIT_DATA).copy()

# 2. Gestion des Tags
unique_tags = set()
for entities in df["entities"]:
    for _, tag in entities:
        unique_tags.add(tag)

tag2id = {tag: i for i, tag in enumerate(sorted(unique_tags))}
id2tag = {i: tag for tag, i in tag2id.items()}

print(f"Tags trouvés : {tag2id}")

# 3. Tokenizer
tokenizer = CamembertTokenizer.from_pretrained(config.MODEL_NAME)

class BottinDataset(Dataset):
    def __init__(self, dataframe, tokenizer, tag2id, max_len):
        self.len = len(dataframe)
        self.data = dataframe
        self.tokenizer = tokenizer
        self.tag2id = tag2id
        self.max_len = max_len

    def __getitem__(self, index):
        row = self.data.iloc[index]
        entities = row["entities"]
        words = [word for word, tag in entities]
        tags = [tag for word, tag in entities]

        tokenized_sentence = []
        labels = []

        for word, label in zip(words, tags):
            tokenized_word = self.tokenizer.tokenize(word)
            n_subwords = len(tokenized_word)
            tokenized_sentence.extend(tokenized_word)
            labels.extend([self.tag2id[label]] * n_subwords)

        # Ajout des tokens spéciaux <s> et </s>
        tokenized_sentence = ["<s>"] + tokenized_sentence[:self.max_len - 2] + ["</s>"]
        labels = [self.tag2id["O"]] + labels[:self.max_len - 2] + [self.tag2id["O"]]

        input_ids = self.tokenizer.convert_tokens_to_ids(tokenized_sentence)
        
        padd_len = self.max_len - len(input_ids)
        input_ids += [self.tokenizer.pad_token_id] * padd_len
        labels += [self.tag2id["O"]] * padd_len
        
        attention_mask = [1 if id != self.tokenizer.pad_token_id else 0 for id in input_ids]

        return {
            'ids': torch.tensor(input_ids, dtype=torch.long),
            'mask': torch.tensor(attention_mask, dtype=torch.long),
            'targets': torch.tensor(labels, dtype=torch.long)
        }

    def __len__(self):
        return self.len
    
# --- INITIALISATION ---
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu") 
if device.type == "mps":
    print("Super ! Ton Mac va utiliser sa puce M1/M2/M3 pour accélérer.")

model = CamembertForTokenClassification.from_pretrained(
    config.MODEL_NAME, 
    num_labels=len(tag2id)
)
model.to(device)

dataset = BottinDataset(df, tokenizer, tag2id, config.MAX_LEN)
dataloader = DataLoader(dataset, batch_size=config.BATCH_SIZE, shuffle=True)

optimizer = AdamW(model.parameters(), lr=config.LEARNING_RATE)

# --- BOUCLE D'ENTRAÎNEMENT ---
print(f"Début de l'entraînement sur {device}...")

model.train()
for epoch in range(config.EPOCHS):
    total_loss = 0
    for batch in tqdm(dataloader, desc=f"Epoch {epoch + 1}"):
        optimizer.zero_grad()
        
        ids = batch['ids'].to(device)
        mask = batch['mask'].to(device)
        targets = batch['targets'].to(device)

        outputs = model(ids, attention_mask=mask, labels=targets)
        loss = outputs.loss
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    print(f"Perte moyenne (Loss): {total_loss / len(dataloader):.4f}")

# --- SAUVEGARDE ---
os.makedirs("../models/camembert_bottin", exist_ok=True)
model.save_pretrained("../models/camembert_bottin")
tokenizer.save_pretrained("../models/camembert_bottin")
print("\nModèle sauvegardé dans ../models/camembert_bottin")