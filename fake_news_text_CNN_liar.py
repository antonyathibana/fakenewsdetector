def train_textcnn():
    from liar_preprocessing import load_and_prepare_data, MAX_SEQUENCE_LENGTH, MAX_VOCAB_SIZE
    import tensorflow as tf
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Embedding, Conv1D, GlobalMaxPooling1D, Concatenate, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    import matplotlib.pyplot as plt
    import random
    import numpy as np
    from tensorflow.keras.regularizers import l2
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

    # Set seeds for reproducibility
    tf.random.set_seed(42)
    np.random.seed(42)
    random.seed(42)

    # Load data
    X_train, X_val, X_test, y_train, y_val, y_test, tokenizer = load_and_prepare_data()

    # Model hyperparameters
    embedding_dim = 300
    filter_sizes = [5]
    num_filters = 128
    dropout_rate = 0.5
    max_length = MAX_SEQUENCE_LENGTH
    max_vocab_size = MAX_VOCAB_SIZE

    # Input and embedding layer
    input_layer = Input(shape=(max_length,))
    embedding = Embedding(input_dim=max_vocab_size, output_dim=embedding_dim)(input_layer)

    # Convolution + Pooling layers
    conv_blocks = []
    for size in filter_sizes:
        conv = Conv1D(filters=num_filters, kernel_size=size, activation='relu',
                      kernel_regularizer=l2(0.01))(embedding)
        pool = GlobalMaxPooling1D()(conv)
        conv_blocks.append(pool)

    concat = Concatenate()(conv_blocks)
    dropout = Dropout(dropout_rate)(concat)
    output = Dense(1, activation='sigmoid')(dropout)

    model = Model(inputs=input_layer, outputs=output)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Callbacks
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True
    )
    lr_scheduler = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2,
        min_lr=0.0001
    )

    # Training
    history = model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=64,
        validation_data=(X_val, y_val),
        callbacks=[early_stopping, lr_scheduler]
    )

    # Evaluation
    val_loss, val_acc = model.evaluate(X_val, y_val)
    print(f"Validation Accuracy: {val_acc:.4f}")

    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {test_acc:.4f}")

    # Accuracy Plot
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('TextCNN Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig("textcnn_liars_accuracy.png")
    plt.close()

    # Loss Plot
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('TextCNN Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig("textcnn_liars_loss.png")
    plt.close()

    # Confusion Matrix
    y_pred_probs = model.predict(X_test)
    y_pred = (y_pred_probs > 0.5).astype(int).flatten()  # thresholding at 0.5
    cm = confusion_matrix(y_test, y_pred)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Fake", "Reliable"])
    disp.plot(cmap="Blues", values_format='d')
    plt.title('Confusion Matrix (Test Set)')
    plt.savefig("textcnn_liars_confusion_matrix.png")
    plt.close()

    # Save model
    model.save("textcnn_liars_model.keras")

    return model

# Run the training
train_textcnn()
