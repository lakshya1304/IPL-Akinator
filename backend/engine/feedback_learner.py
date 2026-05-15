import json
import os
from pathlib import Path


# Get base directory for database files
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

LEARN_FILE = DATABASE_DIR / "learned_patterns.json"


def load_patterns():

    if not LEARN_FILE.exists():

        return []

    with open(
        LEARN_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_failure(
    history,
    guessed,
    correct
):

    data = load_patterns()

    data.append({

        "history": history,

        "wrong_guess": guessed,

        "correct_player": correct
    })

    with open(
        LEARN_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )