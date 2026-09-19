DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]


def increase_difficulty(current_difficulty):
    """
    Increase one level.
    Easy -> Medium -> Hard
    """
    if current_difficulty == "Easy":
        return "Medium"

    if current_difficulty == "Medium":
        return "Hard"

    return "Hard"


def decrease_difficulty(current_difficulty):
    """
    Decrease one level.
    Hard -> Medium -> Easy
    """
    if current_difficulty == "Hard":
        return "Medium"

    if current_difficulty == "Medium":
        return "Easy"

    return "Easy"


def decide_next_difficulty(current_difficulty, recent_attempts):
    """
    Decide the next puzzle difficulty.

    recent_attempts is a list like:
    [{"correct": True}, {"correct": True}, {"correct": True}]
    """

    # If fewer than 3 puzzles are attempted, keep the same difficulty.
    if len(recent_attempts) < 3:
        return current_difficulty

    # Take only the latest three results.
    last_three = recent_attempts[-3:]
    results = [attempt["correct"] for attempt in last_three]

    # All three answers are correct.
    if results == [True, True, True]:
        return increase_difficulty(current_difficulty)

    # All three answers are wrong.
    if results == [False, False, False]:
        return decrease_difficulty(current_difficulty)

    # Mixed results: no difficulty change.
    return current_difficulty


if __name__ == "__main__":
    # Test 1: Three correct answers.
    test_1 = [
        {"correct": True},
        {"correct": True},
        {"correct": True}
    ]
    print("Easy + 3 correct =", decide_next_difficulty("Easy", test_1))

    # Test 2: Three wrong answers.
    test_2 = [
        {"correct": False},
        {"correct": False},
        {"correct": False}
    ]
    print("Medium + 3 wrong =", decide_next_difficulty("Medium", test_2))

    # Test 3: Mixed answers.
    test_3 = [
        {"correct": True},
        {"correct": False},
        {"correct": True}
    ]
    print("Medium + mixed answers =", decide_next_difficulty("Medium", test_3))

    # Test 4: Hard cannot increase further.
    test_4 = [
        {"correct": True},
        {"correct": True},
        {"correct": True}
    ]
    print("Hard + 3 correct =", decide_next_difficulty("Hard", test_4))