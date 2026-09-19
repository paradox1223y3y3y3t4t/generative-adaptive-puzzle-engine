# Generative Adaptive Puzzle Engine with Learner Modeling and Difficulty Control

## 📌 Project Overview

The Generative Adaptive Puzzle Engine is a web-based puzzle application developed using Python and Flask.

The system generates puzzles for learners and adjusts the puzzle difficulty according to their recent performance.

The main purpose of the project is to provide a simple adaptive learning environment where learners can solve puzzles, receive immediate feedback, and get puzzles at an appropriate difficulty level.

---

## 🎯 Objectives

The main objectives of this project are:

- To generate different types of puzzles.
- To provide Easy, Medium, and Hard difficulty levels.
- To allow users to create an account and log in.
- To record puzzle attempts and results.
- To calculate learner performance.
- To adapt puzzle difficulty according to learner performance.
- To provide a dashboard for tracking progress.
- To provide a final performance report after 10 puzzles.

---

## ⭐ Main Features

### 1. User Registration and Login

Users can create an account and securely log in to the application.

### 2. Puzzle Categories

The system supports five puzzle categories:

- Number Puzzle
- Sequence Puzzle
- Pattern Puzzle
- Logical Reasoning
- Basic Mathematical Puzzle

### 3. Difficulty Levels

Each puzzle can be generated at three difficulty levels:

- Easy
- Medium
- Hard

### 4. Multiple Choice Questions

Each puzzle provides four answer options.

### 5. Timer

The system records the time taken by the learner to answer each puzzle.

### 6. Immediate Feedback

After submitting an answer, the system shows:

- Whether the answer is correct or incorrect
- The selected answer
- The correct answer
- Response time
- Explanation
- Next puzzle difficulty

### 7. Learner Modeling

The system maintains learner performance information such as:

- Total attempts
- Correct answers
- Wrong answers
- Accuracy
- Average response time
- Performance score
- Current difficulty

### 8. Adaptive Difficulty Control

The difficulty level changes according to recent performance.

The basic rule is:

- 3 consecutive correct answers → increase difficulty
- 3 consecutive wrong answers → decrease difficulty
- Mixed results → keep the same difficulty

For example:

```text
Easy → 3 Correct Answers → Medium

Medium → 3 Correct Answers → Hard

Hard → 3 Wrong Answers → Medium