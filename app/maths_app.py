
import streamlit as st

from core.engine.session_manager import (
    initialise_session
)

from core.engine.question_factory import (
    generate_question,
    TOPIC_REGISTRY
)

from core.ui.question_ui import render_question
from core.ui.examples_ui import render_examples
from core.ui.video_ui import render_videos
from core.ui.scaffold_ui import render_scaffold
from core.ui.solution_ui import render_solution

initialise_session()

st.set_page_config(
    page_title="Maths Learning Platform"
)

st.title("📘 Maths Learning Platform")

quiz = st.session_state.quiz

topic = st.selectbox(
    "Choose Topic",
    list(TOPIC_REGISTRY.keys())
)

level = st.slider(
    "Choose Level",
    1,
    5,
    1
)

if st.button("Generate Question"):

    quiz["topic"] = topic
    quiz["level"] = level

    quiz["current_question"] = generate_question(
        topic,
        level
    )

question = quiz.get("current_question")

if question:

    user_answer = render_question(question)

    render_examples(question)

    render_videos(question)

    render_scaffold(question)

    if st.button("Submit Answer"):

        if isinstance(question.correct_answer, dict):

            correct = (
                user_answer ==
                question.correct_answer
            )

        else:

            correct = (
                str(user_answer).strip()
                ==
                str(question.correct_answer)
            )

        if correct:

            st.success("✅ Correct")

        else:

            st.error(
                f"❌ Incorrect. Correct answer: "
                f"{question.correct_answer}"
            )

        render_solution(question)
