import pandas as pd
import re
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Hyperparameters (can be imported too)
MAX_VOCAB_SIZE = 10000
MAX_SEQUENCE_LENGTH = 500

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text

def load_and_prepare_data():
    # Load data, kaggle
    true_df = pd.read_csv("Data/True.csv")
    fake_df = pd.read_csv("Data/Fake.csv")

    # Label data
    true_df['label'] = 1
    fake_df['label'] = 0

    # Combine and shuffle
    data = pd.concat([true_df, fake_df], ignore_index=True).sample(frac=1).reset_index(drop=True)

    # Clean text
    data['clean_text'] = data['text'].apply(clean_text)

    # Tokenize
    tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE, oov_token='<OOV>')
    tokenizer.fit_on_texts(data['clean_text'])
    sequences = tokenizer.texts_to_sequences(data['clean_text'])

    # Pad sequences
    padded = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')

    # First split into train+val and test
    X_temp, X_test, y_temp, y_test = train_test_split(
        padded, data['label'].values, test_size=0.15, stratify=data['label']
    )

    # Then split train and validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.15 / 0.85, stratify=y_temp
    )

    return X_train, X_val, X_test, y_train, y_val, y_test, tokenizer