import unittest

from puzzle_generator import generate_puzzle
from difficulty_controller import decide_next_difficulty


class TestPuzzleEngine(unittest.TestCase):

    def test_puzzle_generation(self):
        puzzle = generate_puzzle("Number Puzzle", "Easy")

        self.assertIsNotNone(puzzle)
        self.assertEqual(puzzle["category"], "Number Puzzle")
        self.assertEqual(puzzle["difficulty"], "Easy")
        self.assertEqual(len(puzzle["options"]), 4)

    def test_difficulty_increases_after_three_correct(self):
        recent_attempts = [
            {"correct": True},
            {"correct": True},
            {"correct": True}
        ]

        next_difficulty = decide_next_difficulty(
            "Easy",
            recent_attempts
        )

        self.assertEqual(next_difficulty, "Medium")

    def test_difficulty_decreases_after_three_wrong(self):
        recent_attempts = [
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ]

        next_difficulty = decide_next_difficulty(
            "Hard",
            recent_attempts
        )

        self.assertEqual(next_difficulty, "Medium")


if __name__ == "__main__":
    unittest.main()