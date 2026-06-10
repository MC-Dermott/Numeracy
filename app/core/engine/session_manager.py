
import streamlit as st

def initialise_session():
    if "quiz" not in st.session_state:
        st.session_state.quiz = {
            "topic": None,
            "level": 1,
            "current_question": None,
            "score": 0,
            "mode": "Practice",
            "test_question_num": 0,
            "test_score": 0,
            "test_complete": False,
        }
