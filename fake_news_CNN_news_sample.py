from shared_preprocessing_news_samples import load_and_prepare_data, MAX_SEQUENCE_LENGTH, MAX_VOCAB_SIZE
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Conv1D, GlobalMaxPooling1D, Concatenate, Dense, Dropout
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np

def train_textcnn():
    # Load data
    X_train, X_val, y_train, y_val, tokenizer = load_and_prepare_data()

    # Model hyperparameters
    embedding_dim = 100
    filter_sizes = [3, 4, 5]
    num_filters = 128
    dropout_rate = 0.3
    max_length = MAX_SEQUENCE_LENGTH
    max_vocab_size = MAX_VOCAB_SIZE

    # Model architecture
    input_layer = Input(shape=(max_length,))
    embedding_layer = Embedding(input_dim=max_vocab_size, output_dim=embedding_dim)(input_layer)

    conv_blocks = []
    for size in filter_sizes:
        conv = Conv1D(filters=num_filters, kernel_size=size, activation='relu')(embedding_layer)
        pool = GlobalMaxPooling1D()(conv)
        conv_blocks.append(pool)

    concat = Concatenate()(conv_blocks)
    drop = Dropout(dropout_rate)(concat)
    output = Dense(1, activation='sigmoid')(drop)

    model = Model(inputs=input_layer, outputs=output)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Training
    history = model.fit(
        X_train, y_train,
        epochs=5,
        batch_size=64,
        validation_data=(X_val, y_val)
    )

    # Evaluation
    loss, acc = model.evaluate(X_val, y_val)
    print(f"Validation Accuracy: {acc:.4f}")

    # Plot Accuracy
    plt.figure()
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('TextCNN Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.tight_layout()
    plt.savefig("textcnn_accuracy_news_samples.png")
    plt.close()

    # Plot Loss
    plt.figure()
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('TextCNN Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.tight_layout()
    plt.savefig("textcnn_loss_news_samples.png")
    plt.close()

    # Confusion Matrix
    print("\nGenerating Confusion Matrix on Validation Set...")
    y_pred_probs = model.predict(X_val)
    y_pred = (y_pred_probs > 0.5).astype(int).reshape(-1)

    cm = confusion_matrix(y_val, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Fake", "True"])
    disp.plot(cmap="Blues")
    plt.title("Confusion Matrix (Validation Set)")
    plt.tight_layout()
    plt.savefig("textcnn_confusion_matrix_news_samples.png")
    plt.close()

    # Save model
    model.save("textcnn_model_news_samples.h5")

    return model

if __name__ == "__main__":
    train_textcnn()