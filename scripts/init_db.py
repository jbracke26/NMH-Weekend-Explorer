import os
import json

DATA_FILE = "activities.json"

def init_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "") as f:
            json.dump([], f)

if __name__ == "__main__":
    init_db()
    print("Initialized activities.json")