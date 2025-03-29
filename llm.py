import ollama
import json
import pandas as pd
import os
from pathlib import Path

# Load and prepare training data
df = pd.read_csv("extracted_data/training_data.csv")

# Convert to training format
data = []
for _, row in df.iterrows():
    symptoms = ", ".join([col for col in df.columns if row[col] == 1])
    disease = row["prognosis"]
    data.append({
        "prompt": f"Symptoms: {symptoms}. What is the disease?",
        "response": f"Disease: {disease}. Please consult a healthcare provider for treatment."
    })

# Save training data
with open("training_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("🔄 Training medical diagnosis model...")

try:
    # Create model file
    modelfile = '''FROM mistral:7b-instruct-v0.2-q4_0

PARAMETER temperature 0.7
PARAMETER num_ctx 2048
PARAMETER stop "Human:"

SYSTEM "You are a medical diagnosis assistant trained to identify diseases based on symptoms."

TEMPLATE """
Human: {{.input}}
Assistant: {{.response}}
"""'''

    # Save modelfile
    Path("Modelfile").write_text(modelfile)

    # Create and train model
    os.system("ollama create medical-diagnosis -f Modelfile")

    # Train with examples
    with open("training_data.json") as f:
        training_data = json.load(f)

    for item in training_data:
        ollama.chat(
            model='medical-diagnosis',
            messages=[
                {'role': 'user', 'content': item['prompt']},
                {'role': 'assistant', 'content': item['response']}
            ]
        )

    print("✅ Model training complete!")

except Exception as e:
    print(f"❌ Error: {str(e)}")

finally:
    if os.path.exists("Modelfile"):
        os.remove("Modelfile")