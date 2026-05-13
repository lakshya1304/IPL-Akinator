import math

# =========================================
# INITIALIZE PROBABILITIES
# =========================================

def initialize(players):

    total = len(players)

    probs = {}

    for player in players:

        probs[player["name"]] = 1 / total

    return probs

# =========================================
# ANSWER WEIGHTS
# =========================================

ANSWER_WEIGHTS = {

    "yes": 1.0,

    "no": -1.0,

    "maybe": 0.3,

    "dontknow": 0.0
}

# =========================================
# FEATURE IMPORTANCE
# =========================================

FEATURE_WEIGHTS = {

    "role": 1.5,

    "team": 1.3,

    "nationality": 1.4,

    "captain": 1.6,

    "wicketkeeper": 1.5,

    "finisher": 1.7,

    "spinner": 1.5,

    "fast_bowler": 1.5,

    "all_rounder": 1.5,

    "left_handed": 1.2,

    "aggressive": 1.3,

    "death_bowler": 1.6
}

# =========================================
# SMART MATCH CHECK
# =========================================

def feature_match(player, feature):

    # boolean

    if feature in player:

        return bool(player[feature])

    return False

# =========================================
# UPDATE PROBABILITIES
# =========================================

def update_probabilities(

    players,

    probs,

    feature,

    answer
):

    answer_weight = ANSWER_WEIGHTS.get(

        answer,

        0
    )

    feature_weight = FEATURE_WEIGHTS.get(

        feature,

        1.0
    )

    updated = {}

    for player in players:

        name = player["name"]

        prior = probs[name]

        match = feature_match(

            player,

            feature
        )

        likelihood = 1.0

        # =====================================
        # YES
        # =====================================

        if answer == "yes":

            if match:

                likelihood = (
                    1.8 *
                    feature_weight
                )

            else:

                likelihood = 0.25

        # =====================================
        # NO
        # =====================================

        elif answer == "no":

            if match:

                likelihood = 0.25

            else:

                likelihood = (
                    1.4 *
                    feature_weight
                )

        # =====================================
        # MAYBE
        # =====================================

        elif answer == "maybe":

            if match:

                likelihood = 1.15

            else:

                likelihood = 0.9

        # =====================================
        # DONT KNOW
        # =====================================

        else:

            likelihood = 1.0

        posterior = prior * likelihood

        updated[name] = posterior

    # =========================================
    # NORMALIZE
    # =========================================

    total = sum(updated.values())

    if total == 0:

        total = 1

    for player in updated:

        updated[player] /= total

    return updated