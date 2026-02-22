import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import re
from torch import nn
from tqdm import tqdm


# Common variables
real_labels = ["mostly-true", "true"]
fake_labels = ["false", "pants-fire"]
column_names = [
    "ID", "label", "statement", "subject", "speaker", "job", "state", "party",
    "barely_true", "false", "half_true", "mostly_true", "pants_on_fire",
    "context"
]

def clean(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# === 1. Load and preprocess training data ===
df = pd.read_csv("Data/train.tsv", sep="\t", header=None, names=column_names)
df = df[df["label"].isin(real_labels + fake_labels)].copy()
df["label"] = df["label"].apply(lambda x: 1 if x in real_labels else 0)
df['text'] = df['statement'].apply(clean)

# === 2. Train-validation split ===
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df["text"].tolist(), df["label"].tolist(), test_size=0.2, stratify=df["label"])

# === 3. Tokenization ===
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512)

# === 4. Dataset class ===
class LiarDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()} | {"labels": torch.tensor(self.labels[idx])}
    def __len__(self):
        return len(self.labels)

train_dataset = LiarDataset(train_encodings, train_labels)
val_dataset = LiarDataset(val_encodings, val_labels)

# === 5. Model and optimizer ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
model.to(device)

# Adjust class weights to account for imbalanced data
class_weights = torch.tensor([1.0, 2.0]).to(device)  # Adjust based on class imbalance
criterion = nn.CrossEntropyLoss(weight=class_weights)

optimizer = AdamW(model.parameters(), lr=5e-5)

# === 6. Training ===
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)
epoch_losses = []
epoch_train_accuracies = []  # To store training accuracy for each epoch

for epoch in range(10): 
    model.train()
    total_loss = 0
    correct_predictions = 0
    total_predictions = 0
    loop = tqdm(train_loader, desc=f"Epoch {epoch+1}")
    for batch in loop:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = criterion(outputs.logits, batch['labels'])  # Use `criterion` with class weights
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        loop.set_postfix(loss=loss.item())
        total_loss += loss.item()

        # Calculate training accuracy
        preds = torch.argmax(outputs.logits, dim=1)
        correct_predictions += (preds == batch['labels']).sum().item()
        total_predictions += batch['labels'].size(0)

    avg_loss = total_loss / len(train_loader)
    epoch_losses.append(avg_loss)
    train_accuracy = correct_predictions / total_predictions
    epoch_train_accuracies.append(train_accuracy)

# === Save training loss and accuracy plots ===
# Loss plot
plt.plot(epoch_losses, label="Training Loss")
plt.title("BERT Training Loss (LIAR)")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.savefig("bert_training_loss_liar.png")
plt.close()

# Accuracy plot
plt.plot(epoch_train_accuracies, label="Training Accuracy")
plt.title("BERT Training Accuracy (LIAR)")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.savefig("bert_training_accuracy_liar.png")
plt.close()

# === 7. Validation ===
model.eval()
preds, targets = [], []
with torch.no_grad():
    for batch in val_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        logits = outputs.logits
        preds += torch.argmax(logits, dim=1).cpu().tolist()
        targets += batch["labels"].cpu().tolist()

val_acc = accuracy_score(targets, preds)
print(f"Validation Accuracy: {val_acc:.4f}")

# === 7.1 Save validation classification report ===
report_val = classification_report(targets, preds, digits=4, output_dict=True, zero_division=0)
pd.DataFrame(report_val).transpose().to_csv("bert_validation_report.csv")

# === 8. Test Set Evaluation ===
test_df = pd.read_csv("Data/test.tsv", sep="\t", header=None, names=column_names)
test_df = test_df[test_df["label"].isin(real_labels + fake_labels)].copy()
test_df["label"] = test_df["label"].apply(lambda x: 1 if x in real_labels else 0)
test_df['text'] = test_df['statement'].apply(clean)

test_encodings = tokenizer(test_df['text'].tolist(), truncation=True, padding=True, max_length=512)
test_dataset = LiarDataset(test_encodings, test_df['label'].tolist())
test_loader = DataLoader(test_dataset, batch_size=16)

test_preds, test_targets = [], []
with torch.no_grad():
    for batch in test_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        logits = outputs.logits
        test_preds += torch.argmax(logits, dim=1).cpu().tolist()
        test_targets += batch["labels"].cpu().tolist()

test_acc = accuracy_score(test_targets, test_preds)
print(f"Test Accuracy: {test_acc:.4f}")

# === 8.1 Save test classification report and confusion matrix ===
report_test = classification_report(test_targets, test_preds, digits=4, output_dict=True, zero_division=0)
pd.DataFrame(report_test).transpose().to_csv("bert_test_report.csv")

# Confusion Matrix
ConfusionMatrixDisplay.from_predictions(test_targets, test_preds)
plt.title("Confusion Matrix (Test Set)")
plt.savefig("bert_confusion_matrix.Liar.png")
plt.close()

# === Save model ===
model.save_pretrained('./bert_liar_model')
tokenizer.save_pretrained('./bert_liar_model')
