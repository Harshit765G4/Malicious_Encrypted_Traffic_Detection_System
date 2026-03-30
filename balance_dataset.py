import pandas as pd

df = pd.read_csv("Final_Model_Dataset.csv")

min_count = df["Label"].value_counts().min()

balanced = df.groupby("Label").sample(min_count)

balanced = balanced.sample(frac=1).reset_index(drop=True)

balanced.to_csv("Balanced_Dataset.csv", index=False)

print("Balanced dataset created")
print(balanced["Label"].value_counts())