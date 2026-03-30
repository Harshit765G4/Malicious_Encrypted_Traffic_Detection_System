import pandas as pd
import numpy as np

from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from tensorflow.keras.utils import to_categorical

# Import model architectures
from cnn_model import create_cnn
from gru_model import create_gru
from bigru_model import create_bigru
from cnn_bigru_model import create_cnn_bigru


# -----------------------------
# LOAD DATASET
# -----------------------------
df = pd.read_csv("Dataset_Final_Normalized.csv")

X = df.drop("Label", axis=1).values
y = df["Label"].values

# convert labels to categorical
y = to_categorical(y)

# reshape for deep learning models
X = X.reshape(X.shape[0], X.shape[1], 1)

print("Dataset Shape:", X.shape)


# -----------------------------
# K-FOLD CROSS VALIDATION
# -----------------------------
kfold = KFold(n_splits=10, shuffle=True, random_state=42)


# -----------------------------
# MODELS TO TRAIN
# -----------------------------
models = {
    "CNN": create_cnn,
    "GRU": create_gru,
    "BiGRU": create_bigru,
    "CNN-BiGRU": create_cnn_bigru
}


# -----------------------------
# RESULT STORAGE
# -----------------------------
results = {}


# -----------------------------
# TRAIN MODELS
# -----------------------------
for model_name, model_func in models.items():

    print("\n==============================")
    print("Training Model:", model_name)
    print("==============================")

    accuracy_scores = []
    precision_scores = []
    recall_scores = []
    f1_scores = []

    fold = 1

    for train_index, test_index in kfold.split(X):

        print("Fold:", fold)

        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # build model
        model = model_func((X.shape[1], 1), y.shape[1])

        # train model
        model.fit(
            X_train,
            y_train,
            epochs=10,
            batch_size=32,
            verbose=0
        )

        # predictions
        predictions = model.predict(X_test)

        predictions = np.argmax(predictions, axis=1)
        y_true = np.argmax(y_test, axis=1)

        # evaluation metrics
        acc = accuracy_score(y_true, predictions)
        prec = precision_score(y_true, predictions, average="weighted")
        rec = recall_score(y_true, predictions, average="weighted")
        f1 = f1_score(y_true, predictions, average="weighted")

        accuracy_scores.append(acc)
        precision_scores.append(prec)
        recall_scores.append(rec)
        f1_scores.append(f1)

        fold += 1


    # average results across folds
    results[model_name] = {
        "Accuracy": np.mean(accuracy_scores),
        "Precision": np.mean(precision_scores),
        "Recall": np.mean(recall_scores),
        "F1": np.mean(f1_scores)
    }


# -----------------------------
# PRINT FINAL RESULTS
# -----------------------------
print("\n\n===================================")
print("FINAL MODEL COMPARISON RESULTS")
print("===================================")

for model, metrics in results.items():

    print("\nModel:", model)
    print("Accuracy :", round(metrics["Accuracy"] * 100, 2), "%")
    print("Precision:", round(metrics["Precision"] * 100, 2), "%")
    print("Recall   :", round(metrics["Recall"] * 100, 2), "%")
    print("F1 Score :", round(metrics["F1"] * 100, 2), "%")