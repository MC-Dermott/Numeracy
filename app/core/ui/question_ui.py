
import streamlit as st

def render_question(question):

    st.subheader(question.question_text)

    if isinstance(question.correct_answer, dict):

        hours = st.number_input(
            "Hours",
            min_value=0,
            step=1
        )

        minutes = st.number_input(
            "Minutes",
            min_value=0,
            step=1
        )

        return {
            "hours": int(hours),
            "minutes": int(minutes)
        }

    return st.text_input("Answer")
