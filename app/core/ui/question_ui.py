import streamlit as st

def render_question(question, suffix="default"):

    st.subheader(question.question_text)

    if isinstance(question.correct_answer, dict):

        col1, col2 = st.columns(2)

        with col1:
            hours_raw = st.text_input(
                "Hours",
                value="",
                key=f"hours_{question.level}_{suffix}"
            )

        with col2:
            minutes_raw = st.text_input(
                "Minutes",
                value="",
                key=f"mins_{question.level}_{suffix}"
            )

        hours_str = hours_raw.strip() if hours_raw else ""
        minutes_str = minutes_raw.strip() if minutes_raw else ""

        hours = int(hours_str) if hours_str.isdigit() else 0
        minutes = int(minutes_str) if minutes_str.isdigit() else 0

        return {
            "hours": hours,
            "minutes": minutes
        }

    return st.text_input("Answer", key=f"generic_ans_{question.level}_{suffix}")

