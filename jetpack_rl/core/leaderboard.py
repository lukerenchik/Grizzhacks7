import json
import os

# Path to the leaderboard file.
LEADERBOARD_PATH = "saves/leaderboard.json"

def load_leaderboard():
    """
    Load the leaderboard from the JSON file.
    
    Returns:
        list: A list of dictionaries representing leaderboard entries,
              each with keys 'name' and 'score'. If the file doesn't exist or is
              invalid, returns an empty list.
    """
    if not os.path.exists(LEADERBOARD_PATH):
        return []
    try:
        with open(LEADERBOARD_PATH, "r") as f:
            leaderboard = json.load(f)
            if isinstance(leaderboard, list):
                return leaderboard
            return []
    except json.JSONDecodeError:
        # In case the JSON file is corrupted, return an empty leaderboard.
        return []

def save_score(name, score):
    """
    Save a new score to the leaderboard.
    
    This function appends the new score, sorts the leaderboard in descending order,
    and keeps only the top 10 entries.
    
    Parameters:
        name (str): The player's name.
        score (int or float): The player's score.
    """
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    # Sort by score in descending order.
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    # Keep only the top 10 scores.
    leaderboard = leaderboard[:10]
    
    # Ensure the 'saves' directory exists.
    os.makedirs(os.path.dirname(LEADERBOARD_PATH), exist_ok=True)
    with open(LEADERBOARD_PATH, "w") as f:
        json.dump(leaderboard, f, indent=2)

def print_leaderboard():
    """
    Print the leaderboard in a formatted manner.
    
    If no leaderboard data is available, prints an appropriate message.
    """
    leaderboard = load_leaderboard()
    if not leaderboard:
        print("No leaderboard data available.")
        return

    print("\n🏆 Leaderboard:")
    for idx, entry in enumerate(leaderboard, start=1):
        print(f"{idx}. {entry['name']} - {entry['score']}")

def get_leaderboard():
    """
    Return the leaderboard data.
    
    Returns:
        list: A list of leaderboard entries.
    """
    return load_leaderboard()
