import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Bidirectional, LSTM, Dense, Dropout, Layer
from tensorflow.keras import backend as K
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np
from shared_preprocessing import load_and_prepare_data, MAX_SEQUENCE_LENGTH, MAX_VOCAB_SIZE

# Custom attention layer
class Attention(Layer):
    def __init__(self, **kwargs):
        super(Attention, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name='att_weight', shape=(input_shape[-1], 1),
                                 initializer='random_normal', trainable=True)
        self.b = self.add_weight(name='att_bias', shape=(input_shape[1], 1),
                                 initializer='zeros', trainable=True)
        super(Attention, self).build(input_shape)

    def call(self, inputs):
        e = K.tanh(K.dot(inputs, self.W) + self.b)
        a = K.softmax(e, axis=1)
        output = inputs * a
        return K.sum(output, axis=1)

# Train the model
def train_bilstm_attention():
    # Load data
    X_train, X_val, X_test, y_train, y_val, y_test, tokenizer = load_and_prepare_data()

    # Hyperparameters
    embedding_dim = 100
    lstm_units = 128
    dropout_rate = 0.5

    # Model
    input_layer = Input(shape=(MAX_SEQUENCE_LENGTH,))
    embedding = Embedding(input_dim=MAX_VOCAB_SIZE, output_dim=embedding_dim, input_length=MAX_SEQUENCE_LENGTH)(input_layer)
    bilstm = Bidirectional(LSTM(units=lstm_units, return_sequences=True))(embedding)
    attention = Attention()(bilstm)
    dropout = Dropout(dropout_rate)(attention)
    output = Dense(1, activation='sigmoid')(dropout)

    model = Model(inputs=input_layer, outputs=output)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train
    history = model.fit(
        X_train, y_train,
        epochs=5,
        batch_size=64,
        validation_data=(X_val, y_val)
    )

    # Validation Evaluation
    val_loss, val_acc = model.evaluate(X_val, y_val)
    print(f"Validation Accuracy: {val_acc:.4f}")

    # Test Evaluation
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {test_acc:.4f}")

    # Save Accuracy Plot
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('BiLSTM + Attention Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig("bilstm_attention_accuracy.png")
    plt.close()

    # Save Loss Plot
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('BiLSTM + Attention Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig("bilstm_attention_loss.png")
    plt.close()

    # Confusion Matrix for Validation Set
    y_val_pred_probs = model.predict(X_val)
    y_val_preds = (y_val_pred_probs > 0.5).astype(int)

    cm_val = confusion_matrix(y_val, y_val_preds)
    disp_val = ConfusionMatrixDisplay(confusion_matrix=cm_val, display_labels=["Fake", "Reliable"])
    disp_val.plot(cmap="Blues")
    plt.title("Confusion Matrix (Validation Set)")
    plt.savefig("bilstm_attention_confusion_matrix_val.png")
    plt.close()

    # Confusion Matrix for Test Set
    y_test_pred_probs = model.predict(X_test)
    y_test_preds = (y_test_pred_probs > 0.5).astype(int)

    cm_test = confusion_matrix(y_test, y_test_preds)
    disp_test = ConfusionMatrixDisplay(confusion_matrix=cm_test, display_labels=["Fake", "Reliable"])
    disp_test.plot(cmap="Blues")
    plt.title("Confusion Matrix (Test Set)")
    plt.savefig("bilstm_attention_confusion_matrix_test.png")
    plt.close()

    return model

if __name__ == "__main__":
    model = train_bilstm_attention()
    model.save("bilstm_attention_model.h5")
