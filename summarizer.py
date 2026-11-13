import os
from transformers import pipeline

print("STARTING DOWNLOAD SPRINT NOW...")

# Set up the storage folder
cache_folder = os.path.join(os.getcwd(), "model_cache")
print("Target folder initialized.")

# 1. Download BART
print("Downloading BART Model (Step 1 of 2)...")
summarizer = pipeline(
    "summarization", 
    model="facebook/bart-large-cnn", 
    model_kwargs={"cache_dir": cache_folder}
)

# 2. Download DistilBERT
print("Downloading DistilBERT Model (Step 2 of 2)...")
classifier = pipeline(
    "text-classification", 
    model="bhadresh-savani/distilbert-base-uncased-emotion", 
    model_kwargs={"cache_dir": cache_folder}
)

print("SUCCESS: All models downloaded completely!")
