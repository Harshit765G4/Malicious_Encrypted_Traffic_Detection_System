# 🔐 Encrypted Traffic Classification

A deep-learning research project for **classifying encrypted network traffic from flow-level metadata**, without inspecting encrypted payload contents. The repository builds a preprocessing pipeline and compares CNN, GRU, BiGRU, and CNN-BiGRU architectures for application-level traffic classification across Windows and Android datasets.

> **Focus:** Encrypted Traffic Analysis • Deep Learning • Network Security • Application Classification • IDS Research

## 🎯 Project Overview

Encrypted traffic prevents traditional payload-based inspection, so this project uses **statistical flow characteristics** instead.

The current pipeline is:

```text
Raw Application Traffic CSVs
        │
        ▼
Dataset Preparation
        │
        ├── Remove identifiers / timestamps
        ├── Assign application labels
        └── Merge datasets
        │
        ▼
Label Encoding
        │
        ▼
Class Balancing
        │
        ▼
StandardScaler Normalization
        │
        ▼
Deep Learning Input Reshaping
        │
        ▼
┌────────┬────────┬─────────┬────────────┐
│  CNN   │  GRU   │  BiGRU  │ CNN-BiGRU  │
└────────┴────────┴─────────┴────────────┘
        │
        ▼
10-Fold Cross-Validation
        │
        ▼
Accuracy / Precision / Recall / F1
```

## ✨ Key Features

- **Payload-independent classification:** Uses flow statistics instead of encrypted packet contents.
- **Multi-platform data:** Includes Android and Windows traffic captures.
- **Known/unknown application classes:** Models application identity in an open-world-style classification setup.
- **Four architectures:** CNN, GRU, BiGRU, and CNN-BiGRU.
- **Balanced training set:** Down-samples every class to the size of the smallest class.
- **Standardized features:** Uses `StandardScaler` before deep-learning training.
- **10-fold evaluation:** Uses shuffled K-fold cross-validation with `random_state=42`.

## 📊 Dataset

The repository contains traffic CSVs for Windows and Android devices.

### Known applications

| Platform | Applications represented |
|---|---|
| Android | Chrome, WhatsApp, YouTube |
| Windows | Brave, Chrome, Firefox |

Additional files represent **Unknown** traffic for both platforms.

Dataset files include:

```text
dataset/
├── Android_Known_Chrome.csv
├── Android_Known_WhatsApp.csv
├── Android_Known_YouTube.csv
├── Android_Unknown.csv
├── Windows_Known_Brave.csv
├── Windows_Known_Chrome.csv
├── Windows_Known_Firefox.csv
└── Windows_Unknown.csv
```

## 🧹 Preprocessing Pipeline

### 1. Dataset preparation

`prepare_dataset.py` loads every CSV under `dataset/` and removes network/session identifiers that should not be used directly as model features:

- `src_ip`
- `dst_ip`
- `src_port`
- `dst_port`
- `protocol`
- `timestamp`

Labels are derived from filenames:

| Label | Assigned class name |
|---:|---|
| — | Brave |
| — | Chrome |
| — | Firefox |
| — | Unknown |
| — | WhatsApp |
| — | YouTube |

The script concatenates the input data, drops duplicates, fills missing values with zero, and writes:

```text
Final_Cleaned_Dataset.csv
```

### 2. Label encoding

`encode_dataset.py` converts string labels to numeric class IDs using `LabelEncoder`.

The recorded run shows the classes as:

```text
['Brave' 'Chrome' 'Firefox' 'Unknown' 'WhatsApp' 'YouTube']
```

This produces:

```text
Final_Model_Dataset.csv
```

### 3. Class balancing

`balance_dataset.py` finds the smallest class and samples the same number of examples from every class.

The recorded run produced:

```text
Brave     175
Chrome    175
Firefox   175
Unknown   175
WhatsApp  175
YouTube   175
```

Total balanced samples: **1,050**.

The result is stored as:

```text
Balanced_Dataset.csv
```

### 4. Feature normalization

`normalize_dataset.py` separates the label column, applies `StandardScaler` to all feature columns, and writes:

```text
Dataset_Final_Normalized.csv
```

### 5. Deep-learning input shape

`train_models.py` converts the normalized feature matrix into:

```text
(samples, features, 1)
```

The recorded run reports:

```text
Dataset Shape: (1050, 76, 1)
```

That means the current model input contains **76 normalized features per flow**.

## 🤖 Models

### CNN

`cnn_model.py` implements a 1D convolutional network:

```text
Conv1D(64, kernel=3, ReLU)
        ↓
MaxPooling1D(2)
        ↓
Conv1D(128, kernel=3, ReLU)
        ↓
MaxPooling1D(2)
        ↓
Flatten
        ↓
Dense(128, ReLU)
        ↓
Softmax output
```

### GRU

`gru_model.py` uses a single GRU layer:

```text
GRU(64)
   ↓
Dense(64, ReLU)
   ↓
Softmax output
```

### BiGRU

`bigru_model.py` wraps a 64-unit GRU in a bidirectional layer:

```text
Bidirectional(GRU(64))
          ↓
Dense(64, ReLU)
          ↓
Softmax output
```

### CNN-BiGRU

`cnn_bigru_model.py` combines convolutional feature extraction with bidirectional recurrent processing:

```text
Conv1D(64, kernel=3, ReLU)
        ↓
MaxPooling1D(2)
        ↓
Bidirectional(GRU(64))
        ↓
Dense(64, ReLU)
        ↓
Softmax output
```

## 🔬 Training Procedure

`train_models.py` trains all four architectures using:

- **10-fold K-fold cross-validation**
- `shuffle=True`
- `random_state=42`
- **10 epochs per fold**
- **batch size: 32**
- Adam optimizer
- categorical cross-entropy

For each fold, the script calculates:

- Accuracy
- Weighted precision
- Weighted recall
- Weighted F1

The final reported metrics are the averages across the 10 folds.

## 📈 Recorded Results

The repository includes a recorded `terminalOutput.txt` from the training run on the balanced dataset.

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| **CNN** | **57.71%** | **60.06%** | **57.71%** | **55.04%** |
| GRU | 38.86% | 35.24% | 38.86% | 33.53% |
| BiGRU | 50.29% | 49.78% | 50.29% | 47.33% |
| CNN-BiGRU | 53.62% | 56.85% | 53.62% | 50.82% |

### Interpretation

On this recorded run:

- **CNN is the strongest of the four models** by accuracy, precision, recall, and F1.
- CNN-BiGRU performs better than GRU and BiGRU, but does not outperform CNN.
- The results are substantially lower than the older performance claims that were previously present in the README.

These numbers should be treated as **recorded experiment results**, not as a newly rerun benchmark during this documentation update.

## 📁 Repository Structure

```text
EncryptedDataDetection/
├── dataset/
│   ├── Android_Known_*.csv
│   ├── Android_Unknown.csv
│   ├── Windows_Known_*.csv
│   └── Windows_Unknown.csv
├── prepare_dataset.py
├── encode_dataset.py
├── balance_dataset.py
├── normalize_dataset.py
├── train_models.py
├── cnn_model.py
├── gru_model.py
├── bigru_model.py
├── cnn_bigru_model.py
├── Final_Cleaned_Dataset.csv
├── Final_Model_Dataset.csv
├── Balanced_Dataset.csv
├── Dataset_Final_Normalized.csv
├── terminalOutput.txt
└── README.md
```

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| Python | Data processing and training |
| Pandas | CSV loading and preprocessing |
| NumPy | Numerical operations |
| Scikit-learn | Encoding, scaling, metrics, K-fold splitting |
| TensorFlow / Keras | CNN, GRU, and BiGRU model training |

## 🚀 Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install the dependencies used by the scripts:

```bash
pip install pandas numpy scikit-learn tensorflow
```

## ▶️ Run the Pipeline

Run the scripts from the repository root in this order:

### 1. Prepare the merged dataset

```bash
python prepare_dataset.py
```

### 2. Encode labels

```bash
python encode_dataset.py
```

### 3. Balance classes

```bash
python balance_dataset.py
```

### 4. Normalize features

```bash
python normalize_dataset.py
```

### 5. Train and evaluate models

```bash
python train_models.py
```

## ⚠️ Current Limitations

The repository is a research/learning implementation and has several limitations:

- The current balanced dataset contains only **1,050 samples**.
- Training uses 76 normalized features without a learned sequence representation beyond treating the feature vector as a 1D input sequence.
- `StandardScaler` is fitted before cross-validation, which means scaling is performed using the complete balanced dataset rather than independently inside each training fold. This can introduce data leakage into cross-validation results.
- The model code emits Keras warnings because `input_shape` is passed directly into layers instead of using an explicit `Input` layer.
- Some folds produce undefined-precision warnings when a class receives no predicted samples.
- No model checkpoints are saved by the current training script.
- The repository does not currently include automated hyperparameter search.
- The raw and intermediate CSV files are relatively large for a source repository.

## 🔬 Recommended Improvements

### Evaluation

- Fit the scaler separately inside each training fold.
- Use `StratifiedKFold` instead of plain `KFold` for multiclass classification.
- Add confusion matrices and per-class precision/recall/F1.
- Report mean ± standard deviation across folds.
- Add a held-out test set that is never used during model selection.

### Modeling

- Add dropout and regularization.
- Tune convolution kernel sizes and recurrent units.
- Compare deeper CNN/GRU variants.
- Try attention mechanisms.
- Evaluate transformer-based sequence models.
- Investigate whether the 76-feature ordering has enough semantic meaning for convolution/recurrent layers.

### Data

- Collect more traffic sessions.
- Increase application diversity.
- Separate device-specific effects from application identity.
- Add temporal/session-level aggregation.
- Evaluate domain shift between Android and Windows traffic.

## 📌 Research Direction

The project can be extended toward a more robust encrypted-traffic IDS by combining:

```text
Flow-level statistical features
          +
Cross-device / cross-platform evaluation
          +
Temporal traffic representations
          +
Attention / Transformer models
          +
Open-world unknown-application detection
          ↓
Robust Encrypted-Traffic IDS
```

## 📄 License

No `LICENSE` file is currently present in the repository, so no formal open-source license should be assumed.

## 👨‍💻 Author

**Harshit Garg**

GitHub: [@Harshit765G4](https://github.com/Harshit765G4)

---

🔐 **EncryptedDataDetection** — learning and experimenting with deep-learning-based encrypted traffic classification without relying on payload inspection.