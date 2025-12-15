import pickle
import os

DATA_FILE = "users_data.pkl"

def load_users():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        return []

def save_users(users):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(users, f)
