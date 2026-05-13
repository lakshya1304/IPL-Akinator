def explain(player, players, answers):
    for p in players:
        if p["name"] == player:
            matched = []
            for key, val in answers.items():
                if p[key] == val:
                    matched.append(key)

            return f"Matched features: {', '.join(matched)}"