def grade(state, task="easy"):
    """
    Grades the financial health of the agent.
    Returns a score strictly between 0 and 1.
    """
    savings = state.get("savings", 0)
    balance = state.get("balance", 0)
    goal = state.get("goal", 1000)

    # Base score starts in the middle
    score = 0.5 

    # 1. Savings Progress (weighted +0.3 to -0.3)
    progress = savings / goal
    if progress >= 1.0:
        score += 0.3
    elif progress > 0.5:
        score += 0.1
    else:
        score -= 0.2

    # 2. Stability Bonus
    if balance > 200:
        score += 0.1
    else:
        score -= 0.2

    # 3. Task Differentiation
    # This ensures "easy", "medium", and "hard" generate different scoring paths
    if task == "easy":
        score += 0.02
    elif task == "medium":
        score += 0.01
    else:
        score -= 0.02

    # 🚨 CRITICAL FIX: The "Strictly Between 0 and 1" Rule
    # We use 0.01 and 0.99 as buffers.
    return max(0.01, min(0.99, score))