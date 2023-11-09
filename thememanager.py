import os
import json
import dbmanager

themes = dict()

for file in os.listdir("themes/"):
  with open(f"themes/{file}", "r") as f:  # Open each file in read mode
    themes[file[:-5]] = json.loads(
        f.read())  # Store themes in the dictionary using file name as the key


def get_theme(chat_id: int):
  theme_id = dbmanager.get_data(chat_id, "theme", "standard-dark")
  return themes[theme_id]
