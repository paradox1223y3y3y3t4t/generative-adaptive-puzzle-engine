from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection, initialize_database
from puzzle_generator import generate_puzzle
from learner_model import calculate_learner_statistics
from difficulty_controller import decide_next_difficulty


app = Flask(__name__)
app.secret_key = "puzzle_engine_secret_key_2026"

initialize_database()


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for("register"))

        connection = get_connection()
        cursor = connection.cursor()

        try:
            hashed_password = generate_password_hash(password)

            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )

            user_id = cursor.lastrowid

            cursor.execute(
                "INSERT INTO learner_profiles (user_id, current_difficulty) VALUES (?, ?)",
                (user_id, "Easy")
            )

            connection.commit()

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))

        except Exception:
            connection.rollback()
            flash("This email is already registered.", "danger")
            return redirect(url_for("register"))

        finally:
            connection.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()
        connection.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for("login"))

    connection = get_connection()
    cursor = connection.cursor()

    # Get learner profile information.
    cursor.execute(
        "SELECT * FROM learner_profiles WHERE user_id = ?",
        (session["user_id"],)
    )

    profile = cursor.fetchone()

    # Get all attempts for the dashboard chart.
    cursor.execute(
        """
        SELECT correct, difficulty
        FROM attempts
        WHERE user_id = ?
        ORDER BY id
        """,
        (session["user_id"],)
    )

    attempt_rows = cursor.fetchall()
    connection.close()

    difficulty_counts = {
        "Easy": 0,
        "Medium": 0,
        "Hard": 0
    }

    for row in attempt_rows:
        difficulty = row["difficulty"]

        if difficulty in difficulty_counts:
            difficulty_counts[difficulty] += 1

    chart_data = {
        "correct": profile["correct_answers"],
        "wrong": profile["wrong_answers"],
        "easy": difficulty_counts["Easy"],
        "medium": difficulty_counts["Medium"],
        "hard": difficulty_counts["Hard"]
    }

    return render_template(
        "dashboard.html",
        user_name=session["user_name"],
        profile=profile,
        chart_data=chart_data
    )


@app.route("/puzzle", methods=["POST"])
def puzzle():
    if "user_id" not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for("login"))

    category = request.form.get("category")

    valid_categories = [
        "Number Puzzle",
        "Sequence Puzzle",
        "Pattern Puzzle",
        "Logical Reasoning",
        "Basic Mathematical Puzzle"
    ]

    if category not in valid_categories:
        flash("Please select a valid puzzle category.", "danger")
        return redirect(url_for("dashboard"))

    # Start a NEW 10-puzzle session.
    session["selected_category"] = category
    session["puzzle_count"] = 0
    session["session_correct"] = 0
    session["session_wrong"] = 0
    session["session_response_times"] = []

    # Remove any previous final result.
    session.pop("final_result", None)

    return create_next_puzzle(category)


@app.route("/next_puzzle")
def next_puzzle():
    if "user_id" not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for("login"))

    category = session.get("selected_category")

    if not category:
        flash("Please select a puzzle category first.", "danger")
        return redirect(url_for("dashboard"))

    # Prevent an 11th puzzle after the final result.
    if session.get("puzzle_count", 0) >= 10:
        return redirect(url_for("final_result"))

    return create_next_puzzle(category)


def create_next_puzzle(category):
    """Create a new puzzle using the learner's current difficulty."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT current_difficulty FROM learner_profiles WHERE user_id = ?",
        (session["user_id"],)
    )

    profile = cursor.fetchone()
    connection.close()

    difficulty = profile["current_difficulty"]

    generated_puzzle = generate_puzzle(category, difficulty)

    session["current_puzzle"] = generated_puzzle

    return render_template(
        "puzzle.html",
        puzzle=generated_puzzle
    )


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    if "user_id" not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for("login"))

    puzzle = session.get("current_puzzle")

    if not puzzle:
        flash(
            "No active puzzle found. Please start a new puzzle.",
            "danger"
        )
        return redirect(url_for("dashboard"))

    selected_answer = request.form.get("selected_answer")

    if not selected_answer:
        flash("Please select an answer.", "danger")
        return redirect(url_for("dashboard"))

    response_time = float(
        request.form.get("response_time", 0)
    )

    is_correct = selected_answer == puzzle["answer"]

    connection = get_connection()
    cursor = connection.cursor()

    # Save the puzzle in SQLite.
    cursor.execute(
        """
        INSERT INTO puzzles (
            question,
            category,
            difficulty,
            option1,
            option2,
            option3,
            option4,
            correct_answer,
            explanation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            puzzle["question"],
            puzzle["category"],
            puzzle["difficulty"],
            puzzle["options"][0],
            puzzle["options"][1],
            puzzle["options"][2],
            puzzle["options"][3],
            puzzle["answer"],
            puzzle["explanation"]
        )
    )

    puzzle_id = cursor.lastrowid

    # Save the learner's answer.
    cursor.execute(
        """
        INSERT INTO attempts (
            user_id,
            puzzle_id,
            selected_answer,
            correct,
            response_time,
            difficulty,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session["user_id"],
            puzzle_id,
            selected_answer,
            int(is_correct),
            response_time,
            puzzle["difficulty"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    # Get all attempts for learner-model calculations.
    cursor.execute(
        """
        SELECT correct, response_time
        FROM attempts
        WHERE user_id = ?
        """,
        (session["user_id"],)
    )

    attempt_rows = cursor.fetchall()

    attempts = []

    for row in attempt_rows:
        attempts.append(
            {
                "correct": bool(row["correct"]),
                "response_time": row["response_time"]
            }
        )

    statistics = calculate_learner_statistics(attempts)

    # Get the latest three results for adaptive difficulty.
    cursor.execute(
        """
        SELECT correct
        FROM attempts
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 3
        """,
        (session["user_id"],)
    )

    recent_rows = cursor.fetchall()

    recent_attempts = []

    for row in reversed(recent_rows):
        recent_attempts.append(
            {
                "correct": bool(row["correct"])
            }
        )

    # Existing adaptive difficulty system.
    next_difficulty = decide_next_difficulty(
        puzzle["difficulty"],
        recent_attempts
    )

    # Save updated learner statistics and difficulty.
    cursor.execute(
        """
        UPDATE learner_profiles
        SET total_attempts = ?,
            correct_answers = ?,
            wrong_answers = ?,
            accuracy = ?,
            average_response_time = ?,
            performance_score = ?,
            current_difficulty = ?
        WHERE user_id = ?
        """,
        (
            statistics["total_attempts"],
            statistics["correct_answers"],
            statistics["wrong_answers"],
            statistics["accuracy"],
            statistics["average_response_time"],
            statistics["performance_score"],
            next_difficulty,
            session["user_id"]
        )
    )

    connection.commit()
    connection.close()

    # ---------------------------------------------------------
    # 10-PUZZLE SESSION TRACKING
    # ---------------------------------------------------------

    puzzle_count = session.get("puzzle_count", 0) + 1
    session["puzzle_count"] = puzzle_count

    if is_correct:
        session["session_correct"] = (
            session.get("session_correct", 0) + 1
        )
    else:
        session["session_wrong"] = (
            session.get("session_wrong", 0) + 1
        )

    response_times = session.get(
        "session_response_times",
        []
    )

    response_times.append(response_time)

    session["session_response_times"] = response_times

    # ---------------------------------------------------------
    # FINAL RESULT AFTER PUZZLE 10
    # ---------------------------------------------------------

    if puzzle_count == 10:

        session_correct = session.get(
            "session_correct",
            0
        )

        session_wrong = session.get(
            "session_wrong",
            0
        )

        session_response_times = session.get(
            "session_response_times",
            []
        )

        total_questions = 10

        accuracy = (
            session_correct / total_questions
        ) * 100

        if session_response_times:
            average_response_time = (
                sum(session_response_times)
                / len(session_response_times)
            )
        else:
            average_response_time = 0

        # Decide performance level.
        if accuracy >= 90:
            performance_level = "Excellent"
            recommendation = (
                "Excellent performance! "
                "You can continue with challenging puzzles "
                "to improve your problem-solving skills."
            )

        elif accuracy >= 75:
            performance_level = "Good"
            recommendation = (
                "Good performance! "
                "Keep practicing regularly to improve "
                "your accuracy and speed."
            )

        elif accuracy >= 60:
            performance_level = "Average"
            recommendation = (
                "Your performance is average. "
                "Practice more puzzles to improve "
                "accuracy and confidence."
            )

        else:
            performance_level = "Needs Improvement"
            recommendation = (
                "Keep practicing! "
                "Focus on understanding the puzzle logic "
                "and solving questions carefully."
            )

        final_result = {
            "total_questions": total_questions,
            "correct_answers": session_correct,
            "wrong_answers": session_wrong,
            "accuracy": round(accuracy, 2),
            "average_response_time": round(
                average_response_time,
                2
            ),
            "final_difficulty": next_difficulty,
            "performance_level": performance_level,
            "recommendation": recommendation
        }

        session["final_result"] = final_result

        # Remove the current puzzle because the session is finished.
        session.pop("current_puzzle", None)

        return redirect(url_for("final_result"))

    # ---------------------------------------------------------
    # NORMAL RESULT FOR PUZZLES 1 TO 9
    # ---------------------------------------------------------

    result = {
        "selected_answer": selected_answer,
        "correct": is_correct,
        "correct_answer": puzzle["answer"],
        "response_time": round(response_time, 2),
        "explanation": puzzle["explanation"],
        "category": puzzle["category"],
        "difficulty": puzzle["difficulty"],
        "next_difficulty": next_difficulty,
        "puzzle_number": puzzle_count
    }

    return render_template(
        "result.html",
        result=result
    )


@app.route("/final_result")
def final_result():
    if "user_id" not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for("login"))

    result = session.get("final_result")

    if not result:
        flash(
            "You have not completed a 10-puzzle session yet.",
            "info"
        )
        return redirect(url_for("dashboard"))

    return render_template(
        "final_result.html",
        user_name=session["user_name"],
        result=result
    )


@app.route("/logout")
def logout():
    session.clear()

    flash("You have logged out.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)