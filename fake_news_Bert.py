import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, get_scheduler
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import random

# 0. Set seeds for reproducibility
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(42)

# 1. Load and prep data
df_true = pd.read_csv("Data/True.csv")
df_fake = pd.read_csv("Data/Fake.csv")

df_true["label"] = 1
df_fake["label"] = 0
df = pd.concat([df_true, df_fake], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)

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
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.labels)

train_dataset = NewsDataset(train_encodings, train_labels)
val_dataset = NewsDataset(val_encodings, val_labels)
test_dataset = NewsDataset(test_encodings, test_labels)

# 5. Model + Optimizer + Scheduler
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
model.to(device)

optimizer = AdamW(model.parameters(), lr=5e-5)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)
test_loader = DataLoader(test_dataset, batch_size=16)

num_training_steps = len(train_loader) * 3  # 3 epochs
lr_scheduler = get_scheduler(
    "linear", optimizer=optimizer,
    num_warmup_steps=int(0.1 * num_training_steps),
    num_training_steps=num_training_steps
)

# 6. Training
train_losses = []
val_losses = []
best_val_acc = 0

for epoch in range(3):
    print(f"\nEpoch {epoch+1}")
    
    # Train
    model.train()
    total_train_loss = 0
    loop = tqdm(train_loader, desc="Training")
    for batch in loop:
        batch = {k: v.to(device) for k, v in batch.items()}
        
        optimizer.zero_grad()
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        lr_scheduler.step()
        
        total_train_loss += loss.item()
        loop.set_postfix(loss=loss.item())
    
    avg_train_loss = total_train_loss / len(train_loader)
    train_losses.append(avg_train_loss)

    # Validation
    model.eval()
    total_val_loss = 0
    val_preds, val_targets = [], []
    with torch.no_grad():
        for batch in tqdm(val_loader, desc="Validation"):
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            logits = outputs.logits
            
            total_val_loss += loss.item()
            val_preds += torch.argmax(logits, dim=1).cpu().tolist()
            val_targets += batch["labels"].cpu().tolist()
    
    avg_val_loss = total_val_loss / len(val_loader)
    val_losses.append(avg_val_loss)

    val_acc = accuracy_score(val_targets, val_preds)
    print(f"Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.4f}")
    
    # Save model if val_acc improves
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        model.save_pretrained('./saved_bert_model')
        tokenizer.save_pretrained('./saved_bert_model')
        print(f"Model saved with new best validation accuracy: {best_val_acc:.4f}")

# Save training/validation loss plot
plt.plot(train_losses, label="Train Loss")
plt.plot(val_losses, label="Validation Loss")
plt.title("BERT Training and Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.savefig("bert_train_val_loss.png")
plt.close()

# 7. Test Predictions
print("\nLoading best model for final testing...")
model = BertForSequenceClassification.from_pretrained('./saved_bert_model').to(device)
tokenizer = BertTokenizer.from_pretrained('./saved_bert_model')

model.eval()
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

# Save test predictions
test_df = pd.DataFrame({
    "text": test_texts,
    "label": test_labels,
    "predictions": test_preds
})
test_df.to_csv("bert_test_predictions.csv", index=False)

# 8. Plot prediction distribution
prediction_counts = pd.Series(test_preds).value_counts().sort_index()
plt.bar(prediction_counts.index, prediction_counts.values, color=['skyblue', 'salmon'])
plt.title("Prediction Distribution (Test Set)")
plt.xlabel("Prediction (0=Fake, 1=True)")
plt.ylabel("Number of Predictions")
plt.xticks([0, 1], ['Fake', 'True'])
plt.savefig("bert_test_prediction_distribution.png")
plt.close()

# 9. Confusion Matrix
cm = confusion_matrix(test_targets, test_preds)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Fake", "True"])
disp.plot(cmap="Blues")
plt.title("Confusion Matrix (Test Set)")
plt.savefig("bert_test_confusion_matrix.png")
plt.close()


print("Test predictions saved to 'bert_test_predictions.csv'")
print("Training/validation loss plot saved to 'bert_train_val_loss.png'")
print("Prediction distribution plot saved to 'bert_test_prediction_distribution.png'")
print("Confusion matrix plot saved to 'bert_test_confusion_matrix.png'")
