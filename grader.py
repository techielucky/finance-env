def grade(state):
    savings = state.get("savings", 0)
    expense = state.get("expense", 0)
    balance = state.get("balance", 0)

    score = 0.0

    # reward savings
    if savings > 0:
        score += 0.4

    # penalty for overspending
    if expense > savings:
        score -= 0.3

    # reward good balance
    if balance > 500:
        score += 0.3

    # clamp between 0 and 1
    return max(0.0, min(1.0, score))