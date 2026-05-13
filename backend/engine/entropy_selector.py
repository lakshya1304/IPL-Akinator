import random

def calculate_entropy_split(players, probs, feature):

    yes = 0
    no = 0

    for p in players:

        name = p["name"]

        if p.get(feature):
            yes += probs[name]
        else:
            no += probs[name]

    return min(yes, no)


def select_best_question(players, probs, asked_features):

    features = set()

    for p in players:
        for k in p.keys():
            if k != "name":
                features.add(k)

    scores = []

    for f in features:

        if f in asked_features:
            continue

        score = calculate_entropy_split(
            players,
            probs,
            f
        )

        scores.append((f, score))

    # sort by best entropy
    scores.sort(key=lambda x: x[1], reverse=True)

    # 🔥 IMPORTANT: take TOP 5 instead of best 1
    top_k = scores[:5] if len(scores) >= 5 else scores

    # 🎲 RANDOM PICK from TOP FEATURES
    chosen = random.choice(top_k)

    return chosen[0]