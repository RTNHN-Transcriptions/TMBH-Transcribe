import os
import json
from tqdm import tqdm

# Path to the Data folder
data_folder = './Data'

# List to store the filtered JSON data
filtered_data = []

# Get a list of all files in the Data folder
files = [f for f in os.listdir(data_folder) if f.startswith('BIBLE') and f.endswith('.json')]

# Iterate over all files in the Data folder
for filename in tqdm(files, desc="Processing files"):
    # Construct the full path to the JSON file
    file_path = os.path.join(data_folder, filename)
    
    # Load the JSON data
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    
    # Extract the desired keys from the JSON data
    filtered_data.append({
        'meta_data': json_data['meta_data'],
        'text': json_data['transcription_data']["text"]
    })

# Path to the output JSON file
output_file = './Data/compiled_data.json'

# Write the filtered data to the output JSON file
with open(output_file, 'w') as file:
    json.dump(filtered_data, file)