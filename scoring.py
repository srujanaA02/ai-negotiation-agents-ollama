def calculate_compromise(history: list, positions: dict) -> float:
    score = 0
    total_turns = len(history)

    concession_keywords = ["agree", "accept", "reduce", "increase access", "strengthen"]

    for round_data in history:
        text = (round_data["usa_proposal"] + " " +
                round_data["china_response"]).lower()

        for keyword in concession_keywords:
            if keyword in text:
                score += 1

    if total_turns == 0:
        return 0.0

    normalized_score = score / (total_turns * len(concession_keywords))

    return min(max(normalized_score, 0.0), 1.0)