import zipfile
import os
import pandas as pd

# Extract ZIP file
zip_path = "archive.zip"
extract_folder = "extracted_data"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

# Load CSV files
df_training = pd.read_csv(os.path.join(extract_folder, "training_data.csv"))
df_diseases = pd.read_csv(os.path.join(extract_folder, "Diseases_Symptoms.csv"))

# Check Data
print(df_training.head())
print(df_diseases.head())
