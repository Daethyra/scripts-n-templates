from transformers import pipeline

# Specify the local path where the model is saved based on your directory structure
local_model_path = "llama-2-13b-chat"  # Contains files like "consolidated.00.pth", "params.json", etc.

# Use pipeline with the local model path
pipe = pipeline("text-generation", model=local_model_path)
