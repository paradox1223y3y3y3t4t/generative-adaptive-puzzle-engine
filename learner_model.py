def calculate_accuracy(total_attempts, correct_answers):
    """
    Calculate accuracy as a percentage.
    Example: 8 correct answers out of 10 = 80%.
    """
    if total_attempts == 0:
        return 0

    return round((correct_answers / total_attempts) * 100, 2)


def calculate_average_time(response_times):
    """
    Calculate the average time taken for puzzles.
    """
    if not response_times:
        return 0

    return round(sum(response_times) / len(response_times), 2)


def calculate_speed_score(average_response_time):
    """
    Convert average response time into a score out of 100.

    10 seconds or less = 100 speed score.
    Slower answers reduce the speed score.
    """
    if average_response_time <= 10:
        return 100

    speed_score = 100 - ((average_response_time - 10) * 5)

    # Keep the score between 0 and 100.
    return round(max(0, min(speed_score, 100)), 2)


def calculate_performance_score(accuracy, speed_score):
    """
    Calculate the final performance score.

    Formula:
    70% importance to accuracy
    30% importance to speed
    """
    score = (accuracy * 0.7) + (speed_score * 0.3)
    return round(score, 2)


def get_performance_level(performance_score):
    """
    Convert a numeric performance score into a learner level.
    """
    if performance_score >= 90:
        return "Excellent"
    elif performance_score >= 75:
        return "Good"
    elif performance_score >= 60:
        return "Average"
    else:
        return "Needs Improvement"


def get_recommendation(performance_score):
    """
    Give a simple recommendation based on learner performance.
    """
    if performance_score >= 90:
        return "Excellent work. You are ready for hard puzzles."
    elif performance_score >= 75:
        return "You are performing well. Try harder puzzles."
    elif performance_score >= 60:
        return "You are improving. Continue practising at the current level."
    else:
        return "Practise easy puzzles to improve your problem-solving skills."


def calculate_learner_statistics(attempts):
    """
    Calculate all learner statistics from a list of attempt dictionaries.

    Each attempt should contain:
    {
        "correct": True or False,
        "response_time": number
    }
    """
    total_attempts = len(attempts)
    correct_answers = sum(1 for attempt in attempts if attempt["correct"])
    wrong_answers = total_attempts - correct_answers

    response_times = [attempt["response_time"] for attempt in attempts]

    accuracy = calculate_accuracy(total_attempts, correct_answers)
    average_response_time = calculate_average_time(response_times)
    speed_score = calculate_speed_score(average_response_time)

    performance_score = calculate_performance_score(
        accuracy,
        speed_score
    )

    performance_level = get_performance_level(performance_score)
    recommendation = get_recommendation(performance_score)

    return {
        "total_attempts": total_attempts,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "accuracy": accuracy,
        "average_response_time": average_response_time,
        "speed_score": speed_score,
        "performance_score": performance_score,
        "performance_level": performance_level,
        "recommendation": recommendation
    }


if __name__ == "__main__":
    # Sample learner answers used only for testing this file.
    sample_attempts = [
        {"correct": True, "response_time": 8},
        {"correct": True, "response_time": 10},
        {"correct": False, "response_time": 15},
        {"correct": True, "response_time": 12},
        {"correct": True, "response_time": 9}
    ]

    statistics = calculate_learner_statistics(sample_attempts)

    print("Learner Statistics")
    print("------------------")

    for key, value in statistics.items():
        print(f"{key}: {value}")