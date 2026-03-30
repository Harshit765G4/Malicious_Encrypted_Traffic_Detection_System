import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("Final_Cleaned_Dataset.csv")

le = LabelEncoder()

df["Label"] = le.fit_transform(df["Label"])

print("Label Classes:")
print(le.classes_)

print("\nLabel Distribution:")
print(df["Label"].value_counts())

df.to_csv("Final_Model_Dataset.csv", index=False)

print("\nLabels encoded successfully")