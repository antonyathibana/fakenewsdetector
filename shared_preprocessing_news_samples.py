import pandas as pd
import re
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Hyperparameters (can be imported too)
MAX_VOCAB_SIZE = 10000
MAX_SEQUENCE_LENGTH = 500

# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)   # Remove punctuation
    text = re.sub(r'\d+', '', text)        # Remove digits
    return text

def load_and_prepare_data():
    # Load data
    df = pd.read_csv("Data/news_sample.csv")

    # Keep only needed columns
    df = df[['content', 'type']].dropna()

    # Clean text
    df['clean_text'] = df['content'].apply(clean_text)

    # Map labels: binary classification (reliable = 1, unreliable/bias = 0)
    df['label'] = df['type'].apply(lambda x: 1 if x.strip().lower() == 'reliable' else 0)

    # Tokenize
    tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE, oov_token='<OOV>')
    tokenizer.fit_on_texts(df['clean_text'])
    sequences = tokenizer.texts_to_sequences(df['clean_text'])

    # Pad sequences
    padded = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')

    # Split into training and validation
    X_train, X_val, y_train, y_val = train_test_split(
        padded, df['label'].values, test_size=0.2, stratify=df['label'], random_state=42)

    return X_train, X_val, y_train, y_val, tokenizer
