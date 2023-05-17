import os
import json
import dbmanager

languages = {} # Dictionary to store language translations

# Iterate over files in the "translations/" directory
for file in os.listdir("translations/"):
    with open(f"translations/{file}", "r") as f: # Open each file in read mode
        languages[file[:2]] = json.loads(f.read()) # Store language translations in the dictionary using file name as the key

def get_language(chat_id):
    id = dbmanager.get_data(chat_id, "language", "en") # Get the language preference for the given chat_id from the database
    return languages[id] # Return the language translations corresponding to the language id
