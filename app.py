import streamlit as st

st.set_page_config(
    page_title="SkillProofAI",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 SkillProofAI")
st.subheader("Programming Skill Assessment")
st.write("Demonstrate your knowledge. Discover your potential.")

st.info(
    "Complete this assessment to evaluate your "
    "programming fundamentals."
)

st.header("👩‍🎓 Student Details")

name = st.text_input("Full Name")
email = st.text_input("Email Address")

st.divider()

questions = [
    {
        "question": "Which data type stores whole numbers in Python?",
        "options": ["float", "int", "str", "bool"],
        "answer": "int"
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "define", "def", "fun"],
        "answer": "def"
    },
    {
        "question": "What is the output of 5 // 2 in Python?",
        "options": ["2.5", "3", "2", "1"],
        "answer": "2"
    },
    {
        "question": "Which loop is commonly used to iterate over a sequence?",
        "options": ["for", "switch", "case", "goto"],
        "answer": "for"
    },
    {
        "question": "Which symbol is used for equality comparison?",
        "options": ["=", "==", "!=", ":="],
        "answer": "=="
    }
]

st.header("💻 Programming Assessment")

answers = []

for index, question in enumerate(questions):
    st.write(f"**Question {index + 1}. {question['question']}**")

    selected = st.radio(
        "Choose your answer:",
        question["options"],
        index=None,
        key=f"question_{index}"
    )

    answers.append(selected)

st.divider()

if st.button("Submit Assessment", type="primary"):

    if not name.strip() or not email.strip():
        st.error("Please enter your name and email.")
    elif any(answer is None for answer in answers):
        st.warning("Please answer all questions.")
    else:
        score = sum(
            1 for i, answer in enumerate(answers)
            if answer == questions[i]["answer"]
        )

        percentage = (score / len(questions)) * 100

        if percentage >= 80:
            level = "Strong Fundamentals"
            feedback = "Excellent! You demonstrate strong programming fundamentals."
        elif percentage >= 60:
            level = "Developing Skills"
            feedback = "Good effort! Practise more programming challenges."
        elif percentage >= 40:
            level = "Beginner"
            feedback = "You are building your foundation. Keep practising."
        else:
            level = "Needs Improvement"
            feedback = "Start with basic programming concepts and practise regularly."

        st.session_state["assessment_result"] = {
            "name": name,
            "email": email,
            "score": score,
            "percentage": percentage,
            "level": level,
            "feedback": feedback
        }

if "assessment_result" in st.session_state:
    result = st.session_state["assessment_result"]

    st.divider()
    st.header("📊 Your Assessment Report")

    st.success("Assessment completed successfully!")

    col1, col2, col3 = st.columns(3)

    col1.metric("Score", f"{result['score']}/5")
    col2.metric("Percentage", f"{result['percentage']:.0f}%")
    col3.metric("Skill Level", result["level"])

    st.progress(result["percentage"] / 100)

    st.subheader("Personalised Feedback")
    st.write(result["feedback"])

    st.caption(
        "This is an initial rule-based assessment prototype. "
        "Results are not yet AI-verified or independently certified."
    )

st.divider()

st.caption("SkillProofAI | Turning Skills Into Proof | Innovation Project")
