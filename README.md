# 🚀 Encrypted Traffic Classification using CNN-BiGRU  
### 🔐 Deep Learning-Based Intrusion Detection System (IDS)

---

## 📌 Overview

With the rapid growth of encrypted internet traffic, traditional intrusion detection techniques based on payload inspection are no longer effective. This project presents a **flow-based deep learning framework** for classifying encrypted network traffic into **known and unknown applications**.

We design and evaluate multiple deep learning models, including a hybrid **CNN-BiGRU architecture**, to identify application-level patterns from encrypted traffic without accessing payload data.

---

## 🎯 Objectives

- Classify encrypted traffic using statistical flow features  
- Detect known vs unknown applications (open-world setting)  
- Compare deep learning architectures (CNN, GRU, BiGRU, CNN-BiGRU)  
- Build a complete IDS pipeline from raw PCAP to model evaluation  

---

## 🧠 Key Idea

Instead of inspecting packet contents (which are encrypted), we analyze:

> 📊 **Traffic behavior using flow-based statistical features**

Each network flow is represented using:

```

<Source IP, Destination IP, Source Port, Destination Port, Protocol>

```

From this, we extract features like:

- Flow duration  
- Packet sizes  
- Inter-arrival time (IAT)  
- Byte and packet rates  
- Forward/Backward traffic statistics  

---

## 🏗️ System Pipeline

```

PCAP Capture → Feature Extraction → Data Cleaning → Encoding → Balancing → Normalization → Model Training → Evaluation

```

---

## 📊 Dataset

### 🔹 Platforms
- Windows  
- Android  

### 🔹 Applications

#### Known Applications
- Chrome  
- Brave  
- Firefox  
- YouTube  
- WhatsApp  

#### Unknown Traffic
- Background traffic  
- Mixed real-world traffic  

---

## ⚙️ Feature Extraction

Tool used:

```

CICFlowMeter

```

Extracted ~75 statistical features such as:

- Flow Duration  
- Flow Bytes/s  
- Flow Packets/s  
- Packet Length Statistics  
- Inter Arrival Time  
- TCP Flags  
- Active/Idle Times  

---

## 🧹 Data Preprocessing

### 1️⃣ Data Cleaning
- Removed non-numeric columns (IP, timestamp)
- Handled missing and infinite values

### 2️⃣ Label Encoding
```

Brave → 0
Chrome → 1
Firefox → 2
Unknown → 3
WhatsApp → 4
YouTube → 5

```

### 3️⃣ Dataset Balancing
- Equal samples per class  
- Prevents bias toward dominant classes  

### 4️⃣ Normalization
- StandardScaler applied  
- Ensures stable training  

---

## 🤖 Models Implemented

| Model | Description |
|------|------|
| CNN | Extracts spatial feature patterns |
| GRU | Captures sequential dependencies |
| BiGRU | Bidirectional temporal learning |
| CNN-BiGRU | Hybrid model (Proposed) |

---

## 🔁 Training Strategy

- **10-Fold Cross Validation**
- Ensures robustness and generalization

---

## 📈 Results (Initial Dataset)

| Model | Accuracy | Precision | Recall | F1 Score |
|------|---------|----------|--------|---------|
| CNN | 88.45% | 89.12% | 88.45% | 88.02% |
| GRU | 82.30% | 83.05% | 82.30% | 81.76% |
| BiGRU | 85.67% | 86.21% | 85.67% | 85.10% |
| CNN-BiGRU | **91.28%** | **92.10%** | **91.28%** | **91.02%** |

---

## 📌 Key Insights

- CNN performs best among baseline models  
- CNN-BiGRU shows improved precision and balanced performance  
- GRU struggles due to limited dataset size  
- Dataset size is the **main limiting factor**  

---

## 📁 Project Structure

```

dataset/
│
├── Android_*.csv
├── Windows_*.csv
│
├── Final_Cleaned_Dataset.csv
├── Dataset_Final_Normalized.csv
├── Final_Model_Dataset.csv
│
├── prepare_dataset.py
├── encode_dataset.py
├── balance_dataset.py
├── normalize_dataset.py
├── train_models.py
│
├── cnn_model.py
├── gru_model.py
├── bigru_model.py
├── cnn_bigru_model.py

````

---

## 🚀 How to Run

### 1️⃣ Install Dependencies
```bash
pip install pandas numpy scikit-learn tensorflow
````

---

### 2️⃣ Prepare Dataset

```bash
python prepare_dataset.py
```

---

### 3️⃣ Encode Labels

```bash
python encode_dataset.py
```

---

### 4️⃣ Balance Dataset

```bash
python balance_dataset.py
```

---

### 5️⃣ Normalize Dataset

```bash
python normalize_dataset.py
```

---

### 6️⃣ Train Models

```bash
python train_models.py
```

---

## 🔬 Research Contribution

* End-to-end encrypted traffic classification pipeline
* Multi-platform dataset (Windows + Android)
* Open-world classification setup
* Comparative study of deep learning models
* Hybrid CNN-BiGRU architecture

---

## ⚠️ Limitations

* Small dataset size (~1050 flows)
* Limited session diversity
* Deep learning models require more data

---

## 🔮 Future Work

* Increase dataset size (ongoing)
* Add more applications (Spotify, Telegram, etc.)
* Implement advanced models:

  * Attention mechanisms
  * Transformer-based architectures
* Real-time IDS deployment

---

## 👨‍💻 Author

**Harshit Garg**

---
