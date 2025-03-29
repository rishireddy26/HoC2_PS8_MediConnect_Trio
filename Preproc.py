import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import zipfile
import os

# Extract ZIP file (if not extracted already)
zip_path = "archive.zip"
extract_folder = "extracted_data"

if not os.path.exists(extract_folder):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

# Define file paths
training_data_path = os.path.join(extract_folder, "training_data.csv")
disease_symptoms_path = os.path.join(extract_folder, "Diseases_Symptoms.csv")

# Check if files exist before loading
if not os.path.exists(training_data_path):
    print(f"❌ ERROR: File not found: {training_data_path}")
    exit()

if not os.path.exists(disease_symptoms_path):
    print(f"❌ ERROR: File not found: {disease_symptoms_path}")
    exit()

# Clean data
def clean_data(df):
    """Clean dataframe while preserving at least some data"""
    print(f"Original shape: {df.shape}")
    
    # Remove any duplicate rows
    df = df.drop_duplicates()
    print(f"Shape after removing duplicates: {df.shape}")
    
    # Instead of dropping all rows with any NA, fill NA values
    df = df.fillna(0)  # Fill numeric NA with 0
    print(f"Shape after handling missing values: {df.shape}")
    
    return df

# Load and clean data
print("\nProcessing training data:")
training_data = pd.read_csv(training_data_path)
training_data = clean_data(training_data)

print("\nProcessing disease symptoms data:")
disease_symptoms = pd.read_csv(disease_symptoms_path)
disease_symptoms = clean_data(disease_symptoms)

# Verify we have data before proceeding
if len(training_data) == 0:
    print("❌ ERROR: No data left after cleaning training_data")
    exit()

# Get feature columns (all except prognosis and unnamed columns)
feature_cols = [col for col in training_data.columns 
               if col != 'prognosis' 
               and not col.startswith('Unnamed')]

print(f"\nSelected {len(feature_cols)} feature columns")

# Encode categorical variables
label_encoder = LabelEncoder()
training_data['prognosis'] = label_encoder.fit_transform(training_data['prognosis'])

# Normalize numerical features
scaler = StandardScaler()
training_data[feature_cols] = scaler.fit_transform(training_data[feature_cols])

# Print processed data info
print("\nProcessed Training Data Info:")
print(f"Number of samples: {len(training_data)}")
print(f"Number of features: {len(feature_cols)}")
print(f"Number of diseases: {len(training_data['prognosis'].unique())}")

# Save processed data
processed_data_path = os.path.join(extract_folder, "processed_training_data.csv")
training_data.to_csv(processed_data_path, index=False)
print(f"\nProcessed data saved to: {processed_data_path}")
