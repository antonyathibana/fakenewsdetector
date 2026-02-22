import pandas as pd
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Hyperparameters
MAX_VOCAB_SIZE = 10000
MAX_SEQUENCE_LENGTH = 500

# 3-class mapping
label_map = {
    'pants-fire': 0,
    'false': 0,
    'barely-true': 0,
    'half-true': 1,
    'mostly-true': 1,
    'true': 1
}

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text

def load_and_prepare_data():
    # Load datasets
    train_df = pd.read_csv("Data/train.tsv", sep="\t", header=None)
    valid_df = pd.read_csv("Data/valid.tsv", sep="\t", header=None)
    test_df = pd.read_csv("Data/test.tsv", sep="\t", header=None)

    # Select necessary columns and rename
    train_df = train_df[[1, 2]]
    valid_df = valid_df[[1, 2]]
    test_df = test_df[[1, 2]]
    train_df.columns = ['label', 'text']
    valid_df.columns = ['label', 'text']
    test_df.columns = ['label', 'text']

    # Filter valid labels and map to 3-class
    train_df = train_df[train_df['label'].isin(label_map)]
    valid_df = valid_df[valid_df['label'].isin(label_map)]
    test_df = test_df[test_df['label'].isin(label_map)]

    train_df['label'] = train_df['label'].map(label_map)
    valid_df['label'] = valid_df['label'].map(label_map)
    test_df['label'] = test_df['label'].map(label_map)

    # Clean text
    train_df['clean_text'] = train_df['text'].apply(clean_text)
    valid_df['clean_text'] = valid_df['text'].apply(clean_text)
    test_df['clean_text'] = test_df['text'].apply(clean_text)

    # Tokenize only on training data
    tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE, oov_token='<OOV>')
    tokenizer.fit_on_texts(train_df['clean_text'])

    # Text to sequences
    X_train = tokenizer.texts_to_sequences(train_df['clean_text'])
    X_val = tokenizer.texts_to_sequences(valid_df['clean_text'])
    X_test = tokenizer.texts_to_sequences(test_df['clean_text'])

    # Padding
    X_train = pad_sequences(X_train, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')
    X_val = pad_sequences(X_val, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')
    X_test = pad_sequences(X_test, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')

    # Labels
    y_train = train_df['label'].astype('float32').values
    y_val = valid_df['label'].astype('float32').values
    y_test = test_df['label'].astype('float32').values

    return X_train, X_val, X_test, y_train, y_val, y_test, tokenizer
