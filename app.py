import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SkillProofAI",
    page_icon="🎯",
    layout="wide"
)

# ---------------- DATABASE ----------------

def get_connection():
    return sqlite3.connect("skillproofai.db")

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                skill TEXT,
                difficulty TEXT,
                score INTEGER,
                total INTEGER,
                percentage REAL,
                level TEXT,
                date TEXT
            )
        """)

initialize_database()

# ---------------- QUESTION BANK ----------------

question_bank = {
    "Beginner": [
        {
            "question": "Which data type stores whole numbers in Python?",
            "options": ["float", "int", "str", "bool"],
            "answer": "int"
        },
        {
            "question": "Which keyword defines a function?",
            "options": ["function", "define", "def", "fun"],
            "answer": "def"
        },
        {
            "question": "What is 5 // 2 in Python?",
            "options": ["2.5", "3", "2", "1"],
            "answer": "2"
        },
        {
            "question": "Which loop iterates over a sequence?",
            "options": ["for", "switch", "case", "goto"],
            "answer": "for"
        },
        {
            "question": "Which operator checks equality?",
            "options": ["=", "==", "!=", ":="],
            "answer": "=="
        }
    ],

    "Intermediate": [
        {
            "question": "What does len([1,2,3]) return?",
            "options": ["2", "3", "4", "1"],
            "answer": "3"
        },
        {
            "question": "Which structure stores key-value pairs?",
            "options": ["List", "Tuple", "Dictionary", "Set"],
            "answer": "Dictionary"
        },
        {
            "question": "What does break do inside a loop?",
            "options": [
                "Skips one iteration",
                "Stops the loop",
                "Restarts the loop",
                "Defines a function"
            ],
            "answer": "Stops the loop"
        },
        {
            "question": "What is the output of 3 ** 2?",
            "options": ["6", "9", "8", "5"],
            "answer": "9"
        },
        {
            "question": "Which keyword handles exceptions?",
            "options": ["try", "check", "error", "catch"],
            "answer": "try"
        }
    ],

    "Advanced": [
        {
            "question": "What is the average time complexity of dictionary lookup?",
            "options": ["O(n)", "O(log n)", "O(1)", "O(n²)"],
            "answer": "O(1)"
        },
        {
            "question": "Which structure follows FIFO?",
            "options": ["Stack", "Queue", "Tree", "Graph"],
            "answer": "Queue"
        },
        {
            "question": "Which concept allows a class to inherit another class?",
            "options": ["Encapsulation", "Inheritance", "Iteration", "Compilation"],
            "answer": "Inheritance"
        },
        {
            "question": "Which algorithm uses divide and conquer?",
            "options": ["Linear Search", "Bubble Sort", "Merge Sort", "Selection Sort"],
            "answer": "Merge Sort"
        },
        {
            "question": "Which data structure is commonly used in recursion?",
            "options": ["Queue", "Stack", "Hash Table", "Graph"],
            "answer": "Stack"
        }
    ]
}

# ---------------- SCORING ----------------

def classify_score(percentage):
    if percentage >= 80:
        return "Advanced Proficiency"
    elif percentage >= 60:
        return "Developing Proficiency"
    elif percentage >= 40:
        return "Basic Proficiency"
    else:
        return "Needs Improvement"

# ---------------- HEADER ----------------

st.title("🎯 SkillProofAI")
st.caption("Turning Skills Into Proof.")

st.markdown(
    "### Demonstrate your abilities. Measure your progress. "
    "Build your skill identity."
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📝 Skill Assessment",
        "💻 Coding Challenge",
        "📊 Student Dashboard"
    ]
)

# ---------------- HOME ----------------

if menu == "🏠 Home":

    st.header("Welcome to SkillProofAI")

    st.write(
        "An innovative skill verification platform that "
        "focuses on practical abilities rather than certificates alone."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Assessment Levels", "3")
    col2.metric("Questions Per Level", "5")
    col3.metric("Skill Categories", "1")

    st.divider()

    st.subheader("Our Innovation")

    st.write("""
    - Practical skill assessment
    - Multiple difficulty levels
    - Automatic performance evaluation
    - Student progress tracking
    - Coding challenge submissions
    - Digital skill reports
    """)

    st.info(
        "Start with Skill Assessment to evaluate your programming knowledge."
    )

# ---------------- SKILL ASSESSMENT ----------------

elif menu == "📝 Skill Assessment":

    st.header("Programming Skill Assessment")

    with st.form("assessment_form"):

        name = st.text_input("Student Name")
        email = st.text_input("Email Address")

        difficulty = st.selectbox(
            "Choose Difficulty Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        st.divider()

        st.subheader(f"{difficulty} Assessment")

        selected_answers = []

        questions = question_bank[difficulty]

        for i, question in enumerate(questions):

            st.write(
                f"**Question {i + 1}: {question['question']}**"
            )

            answer = st.radio(
                "Select your answer",
                question["options"],
                index=None,
                key=f"{difficulty}_{i}"
            )

            selected_answers.append(answer)

        submitted = st.form_submit_button(
            "Submit Assessment",
            type="primary"
        )

    if submitted:

        if not name.strip() or not email.strip():
            st.error("Please enter your name and email.")

        elif "@" not in email or "." not in email:
            st.error("Please enter a valid email address.")

        elif any(answer is None for answer in selected_answers):
            st.warning("Please answer all questions.")

        else:

            score = sum(
                selected_answers[i] == questions[i]["answer"]
                for i in range(len(questions))
            )

            total = len(questions)
            percentage = (score / total) * 100
            level = classify_score(percentage)

            feedback = (
                "Excellent performance! Continue solving practical challenges."
                if percentage >= 80 else
                "Good progress! Practise more to strengthen your skills."
                if percentage >= 60 else
                "Keep learning and practising programming fundamentals."
            )

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with get_connection() as conn:
                conn.execute("""
                    INSERT INTO results
                    (name, email, skill, difficulty, score,
                    total, percentage, level, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    name.strip(),
                    email.strip().lower(),
                    "Programming",
                    difficulty,
                    int(score),
                    total,
                    percentage,
                    level,
                    date
                ))

            st.session_state["latest_result"] = {
                "name": name,
                "score": score,
                "total": total,
                "percentage": percentage,
                "level": level,
                "feedback": feedback
            }

            st.success("Assessment completed successfully!")

    if "latest_result" in st.session_state:

        result = st.session_state["latest_result"]

        st.divider()
        st.header("📊 Assessment Report")

        st.write(f"**Student:** {result['name']}")

        col1, col2, col3 = st.columns(3)

        col1.metric("Score", f"{result['score']}/{result['total']}")
        col2.metric("Percentage", f"{result['percentage']:.0f}%")
        col3.metric("Skill Level", result["level"])

        st.progress(result["percentage"] / 100)

        st.subheader("Personalised Feedback")
        st.write(result["feedback"])

        st.caption(
            "Scores are based on predefined answer keys. "
            "They demonstrate assessment performance, not independent certification."
        )

# ---------------- CODING CHALLENGE ----------------

elif menu == "💻 Coding Challenge":

    st.header("Practical Coding Challenge")

    st.write(
        "Demonstrate your problem-solving approach "
        "through a practical programming task."
    )

    st.info(
        "Challenge: Write a Python program to find the largest "
        "of three numbers."
    )

    student_name = st.text_input(
        "Student Name",
        key="coding_name"
    )

    code = st.text_area(
        "Write your Python solution here",
        height=250,
        placeholder="a = int(input())..."
    )

    if st.button("Submit Coding Solution"):

        if not student_name.strip() or not code.strip():
            st.warning("Enter your name and coding solution.")

        else:
            st.session_state["coding_submission"] = {
                "name": student_name,
                "code": code,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            st.success("Coding solution submitted successfully!")

            st.caption(
                "Your solution is recorded in this session. "
                "Automated code execution and grading are not yet implemented."
            )

# ---------------- STUDENT DASHBOARD ----------------

elif menu == "📊 Student Dashboard":

    st.header("Student Performance Dashboard")

    email_search = st.text_input(
        "Enter your registered email address"
    )

    if st.button("View My Results"):

        if not email_search.strip():
            st.warning("Enter your registered email.")

        else:

            with get_connection() as conn:
                history = pd.read_sql_query(
                    """
                    SELECT date, skill, difficulty, score,
                    total, percentage, level
                    FROM results
                    WHERE email = ?
                    ORDER BY id DESC
                    """,
                    conn,
                    params=(email_search.strip().lower(),)
                )

            if history.empty:
                st.info("No assessment records found.")

            else:

                st.success("Assessment history retrieved.")

                st.dataframe(
                    history,
                    use_container_width=True,
                    hide_index=True
                )

                st.subheader("Performance Overview")

                st.metric(
                    "Assessments Completed",
                    len(history)
                )

                st.metric(
                    "Average Score",
                    f"{history['percentage'].mean():.1f}%"
                )

                chart_data = history.iloc[::-1].set_index("date")

                st.line_chart(chart_data["percentage"])

                csv_data = history.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "Download Assessment History",
                    data=csv_data,
                    file_name="skillproofai_report.csv",
                    mime="text/csv"
                )

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "SkillProofAI | Innovation Project | Turning Skills Into Proof."
)
