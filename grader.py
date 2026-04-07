def grade(state):
    savings = state.get("savings", 0)
    expense = state.get("expense", 0)
    balance = state.get("balance", 0)

    score = 0.0

    # reward savings (max 0.5)
    score += min(savings / 1000, 0.5)

    # penalty for overspending
    if expense > savings:
        score -= 0.3

    # reward stability
    if balance > 300:
        score += 0.3

    return max(0.0, min(1.0, score))