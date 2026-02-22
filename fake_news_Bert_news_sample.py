import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import re
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# 1. Load and prep data
df = pd.read_csv("Data/news_sample.csv")

# Drop rows missing important info
df = df.dropna(subset=['content', 'type'])

# Keep only relevant columns and rename
df = df[['content', 'type']]
df = df.rename(columns={'content': 'text', 'type': 'label'})

# Map the 'label' column into binary: reliable or unknown = 1, everything else = 0
def map_type(t):
    t = str(t).lower()
    return 1 if t in ["reliable", "unknown"] else 0

df['label'] = df['label'].apply(map_type)

# Clean text
def clean(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

df['text'] = df['text'].apply(clean)

# Shuffle data
df = df.sample(frac=1).reset_index(drop=True)

# 2. Split into train (70%), val (15%), test (15%)
train_texts, temp_texts, train_labels, temp_labels = train_test_split(
    df["text"].tolist(), df["label"].tolist(), test_size=0.3, stratify=df["label"], random_state=42)

val_texts, test_texts, val_labels, test_labels = train_test_split(
    temp_texts, temp_labels, test_size=0.5, stratify=temp_labels, random_state=42)

# 3. Tokenize
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512)
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=512)

# 4. Dataset class
class NewsDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()} | {"labels": torch.tensor(self.labels[idx])}

    def __len__(self):
        return len(self.labels)

train_dataset = NewsDataset(train_encodings, train_labels)
val_dataset = NewsDataset(val_encodings, val_labels)
test_dataset = NewsDataset(test_encodings, test_labels)

# 5. Model + Optimizer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
model.to(device)

optimizer = AdamW(model.parameters(), lr=5e-5)

# 6. Training
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)
test_loader = DataLoader(test_dataset, batch_size=16)

epoch_losses = []

for epoch in range(3):
    model.train()
    total_loss = 0
    loop = tqdm(train_loader, desc=f"Epoch {epoch+1}")
    for batch in loop:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        loop.set_postfix(loss=loss.item())
        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    epoch_losses.append(avg_loss)

# Save training loss plot
plt.plot(epoch_losses, label="Training Loss")
plt.title("BERT Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.savefig("bert_training_loss.png")
plt.close()

# 7. Validation accuracy
model.eval()
val_preds, val_targets = [], []
with torch.no_grad():
    for batch in val_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        logits = outputs.logits
        val_preds += torch.argmax(logits, dim=1).cpu().tolist()
        val_targets += batch["labels"].cpu().tolist()

val_acc = accuracy_score(val_targets, val_preds)
print(f"Validation Accuracy: {val_acc:.4f}")

# Save model
model.save_pretrained('./saved_bert_model')
tokenizer.save_pretrained('./saved_bert_model')

# 8. Test predictions
test_preds, test_targets = [], []
with torch.no_grad():
    for batch in test_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        logits = outputs.logits
        test_preds += torch.argmax(logits, dim=1).cpu().tolist()
        test_targets += batch["labels"].cpu().tolist()

# Save test predictions to CSV
test_df = pd.DataFrame({
    "text": test_texts,
    "label": test_labels,
    "predictions": test_preds
})
test_df.to_csv("bert_test_predictions.csv", index=False)

# 9. Prediction distribution plot
prediction_counts = pd.Series(test_preds).value_counts().sort_index()
plt.bar(prediction_counts.index, prediction_counts.values, color=['skyblue', 'salmon'])
plt.title("Prediction Distribution (Test Set)")
plt.xlabel("Prediction (0=Fake, 1=Reliable/Unknown)")
plt.ylabel("Number of Predictions")
plt.xticks([0, 1], ['Fake', 'Reliable/Unknown'])
plt.savefig("bert_test_prediction_distribution_news_sample.png")
plt.close()

print("Test predictions saved to 'bert_test_predictions.csv'")
print("Prediction distribution plot saved to 'bert_test_prediction_distribution.png'")


# 10. Confusion Matrix (Test Set)
cm = confusion_matrix(test_targets, test_preds)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Fake", "Reliable"])
disp.plot(cmap="Blues")
plt.title("Confusion Matrix (Test Set)")
plt.tight_layout()
plt.savefig("bert_confusion_matrix_test_news_sample.png")
plt.close()

print("Confusion matrix plot saved to 'bert_confusion_matrix_test_news_sample.png'")
