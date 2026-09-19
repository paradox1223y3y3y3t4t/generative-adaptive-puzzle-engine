import random


def create_options(correct_answer):
    """
    Create four answer options.
    One option is correct and three are incorrect.
    """
    options = {str(correct_answer)}

    while len(options) < 4:
        difference = random.randint(1, 10)
        wrong_answer = correct_answer + random.choice(
            [-difference, difference]
        )

        if wrong_answer >= 0:
            options.add(str(wrong_answer))

    options_list = list(options)
    random.shuffle(options_list)

    return options_list


def generate_number_puzzle(difficulty):
    """Generate a Number Puzzle."""

    if difficulty == "Easy":
        first_number = random.randint(5, 30)
        second_number = random.randint(1, 20)
        answer = first_number + second_number

        question = f"What is {first_number} + {second_number}?"
        explanation = f"{first_number} + {second_number} = {answer}"

    elif difficulty == "Medium":
        first_number = random.randint(4, 12)
        second_number = random.randint(3, 10)
        answer = first_number * second_number

        question = f"What is {first_number} × {second_number}?"
        explanation = f"{first_number} × {second_number} = {answer}"

    else:
        first_number = random.randint(5, 15)
        second_number = random.randint(3, 10)
        third_number = random.randint(5, 25)
        answer = (first_number * second_number) + third_number

        question = f"Calculate: ({first_number} × {second_number}) + {third_number}"
        explanation = (
            f"{first_number} × {second_number} = {first_number * second_number}, "
            f"then + {third_number} = {answer}"
        )

    return {
        "question": question,
        "options": create_options(answer),
        "answer": str(answer),
        "category": "Number Puzzle",
        "difficulty": difficulty,
        "explanation": explanation
    }


def generate_sequence_puzzle(difficulty):
    """Generate a Sequence Puzzle."""

    if difficulty == "Easy":
        start = random.randint(1, 10)
        step = random.randint(2, 5)
        numbers = [start + (step * i) for i in range(5)]
        answer = numbers[-1] + step

        question = f"Find the next number: {numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}, ?"
        explanation = f"The pattern adds {step} each time. The next number is {answer}."

    elif difficulty == "Medium":
        start = random.randint(2, 5)
        multiplier = random.choice([2, 3])
        numbers = [start]

        for _ in range(3):
            numbers.append(numbers[-1] * multiplier)

        answer = numbers[-1] * multiplier

        question = f"Find the next number: {numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}, ?"
        explanation = f"The pattern multiplies by {multiplier}. The next number is {answer}."

    else:
        start = random.randint(2, 10)
        first_step = random.choice([2, 3, 4])
        steps = [first_step, first_step + 2, first_step + 4, first_step + 6]

        numbers = [start]
        for step in steps:
            numbers.append(numbers[-1] + step)

        next_step = first_step + 8
        answer = numbers[-1] + next_step

        question = f"Find the next number: {numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}, {numbers[4]}, ?"
        explanation = (
            f"The numbers are added by {steps[0]}, {steps[1]}, "
            f"{steps[2]}, {steps[3]}. Next add {next_step}. "
            f"The answer is {answer}."
        )

    return {
        "question": question,
        "options": create_options(answer),
        "answer": str(answer),
        "category": "Sequence Puzzle",
        "difficulty": difficulty,
        "explanation": explanation
    }


def generate_pattern_puzzle(difficulty):
    """Generate a Pattern Puzzle."""

    if difficulty == "Easy":
        start = random.randint(2, 5)
        numbers = [start, start * 2, start * 4, start * 8]
        answer = start * 16

        question = f"Find the missing value: {numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}, ?"
        explanation = f"Each number is multiplied by 2. The answer is {answer}."

    elif difficulty == "Medium":
        start = random.randint(5, 15)
        numbers = [start]
        add_values = [3, 6, 9]

        for value in add_values:
            numbers.append(numbers[-1] + value)

        answer = numbers[-1] + 12

        question = f"Find the missing value: {numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}, ?"
        explanation = "The pattern adds 3, then 6, then 9, then 12. The answer is " + str(answer) + "."

    else:
        start = random.randint(2, 5)
        numbers = [start ** 2, (start + 1) ** 2, (start + 2) ** 2, (start + 3) ** 2]
        answer = (start + 4) ** 2

        question = f"Find the missing value: {numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}, ?"
        explanation = f"These are square numbers. The next value is {start + 4}² = {answer}."

    return {
        "question": question,
        "options": create_options(answer),
        "answer": str(answer),
        "category": "Pattern Puzzle",
        "difficulty": difficulty,
        "explanation": explanation
    }


def generate_logic_puzzle(difficulty):
    """Generate a Logical Reasoning Puzzle."""

    labels = random.sample(["A", "B", "C", "D"], 4)

    if difficulty == "Easy":
        first, second, third = labels[0], labels[1], labels[2]
        answer = first
        question = (
            f"If {first} is greater than {second} and "
            f"{second} is greater than {third}, which is the largest?"
        )
        options = [first, second, third, "Cannot say"]
        explanation = f"{first} is greater than both {second} and {third}, so {first} is largest."

    elif difficulty == "Medium":
        first, second, third = labels[0], labels[1], labels[2]
        answer = third
        question = (
            f"If {first} is taller than {second} and "
            f"{second} is taller than {third}, who is shortest?"
        )
        options = [first, second, third, "All are equal"]
        explanation = f"{third} is shorter than {second}, and {second} is shorter than {first}."

    else:
        first, second, third, fourth = labels
        answer = fourth
        question = (
            f"If {first} is older than {second}, {second} is older than {third}, "
            f"and {third} is older than {fourth}, who is youngest?"
        )
        options = [first, second, third, fourth]
        explanation = f"{fourth} is younger than {third}, {second}, and {first}."

    random.shuffle(options)

    return {
        "question": question,
        "options": options,
        "answer": answer,
        "category": "Logical Reasoning",
        "difficulty": difficulty,
        "explanation": explanation
    }


def generate_math_puzzle(difficulty):
    """Generate a Basic Mathematical Puzzle."""

    if difficulty == "Easy":
        first_number = random.randint(10, 40)
        second_number = random.randint(1, 9)
        answer = first_number - second_number

        question = f"Calculate: {first_number} − {second_number}"
        explanation = f"{first_number} − {second_number} = {answer}"

    elif difficulty == "Medium":
        first_number = random.randint(5, 12)
        second_number = random.randint(4, 12)
        answer = first_number * second_number

        question = f"Calculate: {first_number} × {second_number}"
        explanation = f"{first_number} × {second_number} = {answer}"

    else:
        first_number = random.randint(5, 15)
        second_number = random.randint(5, 15)
        third_number = random.randint(2, 8)
        answer = (first_number + second_number) * third_number

        question = f"Calculate: ({first_number} + {second_number}) × {third_number}"
        explanation = (
            f"{first_number} + {second_number} = {first_number + second_number}, "
            f"then × {third_number} = {answer}"
        )

    return {
        "question": question,
        "options": create_options(answer),
        "answer": str(answer),
        "category": "Basic Mathematical Puzzle",
        "difficulty": difficulty,
        "explanation": explanation
    }


def generate_puzzle(category, difficulty):
    """
    Select the correct puzzle generator based on selected category.
    """
    generators = {
        "Number Puzzle": generate_number_puzzle,
        "Sequence Puzzle": generate_sequence_puzzle,
        "Pattern Puzzle": generate_pattern_puzzle,
        "Logical Reasoning": generate_logic_puzzle,
        "Basic Mathematical Puzzle": generate_math_puzzle
    }

    # Use Number Puzzle if an invalid category is received.
    generator = generators.get(category, generate_number_puzzle)

    return generator(difficulty)


if __name__ == "__main__":
    categories = [
        "Number Puzzle",
        "Sequence Puzzle",
        "Pattern Puzzle",
        "Logical Reasoning",
        "Basic Mathematical Puzzle"
    ]

    for category in categories:
        puzzle = generate_puzzle(category, "Easy")

        print("\n------------------------------")
        print("Category:", puzzle["category"])
        print("Difficulty:", puzzle["difficulty"])
        print("Question:", puzzle["question"])
        print("Options:", puzzle["options"])
        print("Correct Answer:", puzzle["answer"])
        print("Explanation:", puzzle["explanation"])