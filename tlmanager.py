import os
import json
import dbmanager

languages = {}

for file in os.listdir("translations/"):
    with open(f"translations/{file}", "r") as f:
        languages[file[:2]] = json.loads(f.read())

def get_language(chat_id):
    id = dbmanager.get_data(chat_id, "language", "en")
    return languages[id]
