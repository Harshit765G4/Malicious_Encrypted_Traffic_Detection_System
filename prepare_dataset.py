import pandas as pd
import glob
import os

# folder containing CSV files
folder = "dataset"

files = glob.glob(folder + "/*.csv")

cleaned_frames = []

for file in files:
    
    df = pd.read_csv(file)
    
    # remove unwanted columns
    drop_cols = [
        "src_ip","dst_ip","src_port","dst_port",
        "protocol","timestamp"
    ]
    
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    
    filename = os.path.basename(file)
    
    # labeling logic
    if "Chrome" in filename:
        label = "Chrome"
    elif "WhatsApp" in filename:
        label = "WhatsApp"
    elif "YouTube" in filename:
        label = "YouTube"
    elif "Brave" in filename:
        label = "Brave"
    elif "Firefox" in filename:
        label = "Firefox"
    else:
        label = "Unknown"
    
    df["Label"] = label
    
    cleaned_frames.append(df)

# merge all datasets
final_df = pd.concat(cleaned_frames, ignore_index=True)

# remove duplicates
final_df = final_df.drop_duplicates()

# handle missing values
final_df = final_df.fillna(0)

# save final dataset
final_df.to_csv("Final_Cleaned_Dataset.csv", index=False)

print("Dataset prepared successfully")
print("Total samples:", len(final_df))