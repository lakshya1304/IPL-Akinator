import json
import os


LEARN_FILE = (
    "database/learned_patterns.json"
)


def load_patterns():

    if not os.path.exists(
        LEARN_FILE
    ):

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