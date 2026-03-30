import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("Balanced_Dataset.csv")

X = df.drop("Label", axis=1)
y = df["Label"]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

final = pd.DataFrame(X_scaled)
final["Label"] = y

final.to_csv("Dataset_Final_Normalized.csv", index=False)

print("Dataset normalized successfully")