def grade_easy(state):
    # avoid overspending
    if state["expense"] < 500:
        return 1.0
    return 0.3


def grade_medium(state):
    # savings goal
    return min(1.0, state["savings"] / 500)


def grade_hard(state):
    # overall wealth
    total = state["balance"] + state["savings"]
    return min(1.0, total / 1500)