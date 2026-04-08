def grade(state, task="easy"):
    """
    Calculates a score strictly between 0.0 and 1.0.
    Formula: (progress * 0.8) + 0.1 ensures range is [0.1, 0.9].
    """
    savings = state.get("savings", 0)
    goal = state.get("goal", 1000)
    
    # Calculate raw progress ratio (0 to 1)
    ratio = min(max(savings / goal, 0.0), 1.0)
    
    # Transform ratio to [0.1, 0.9]
    score = (ratio * 0.8) + 0.1
    
    # Add a tiny task-based offset to ensure the 3 tasks have unique scores
    if task == "medium":
        score += 0.02
    elif task == "hard":
        score += 0.04
        
    return round(score, 3)