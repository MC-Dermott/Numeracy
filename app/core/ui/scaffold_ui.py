import streamlit as st


def is_correct_answer(user_input, correct_answer):
    try:
        return round(float(user_input), 4) == round(float(correct_answer), 4)

    except ValueError:
        return (
            str(user_input).strip().lower()
            ==
            str(correct_answer).strip().lower()
        )

def render_scaffold(question, suffix=""):
    user_answers = []

    for i, step in enumerate(question.scaffold_steps):

        key = f"scaffold_{suffix}_{i}"

        st.write(step["prompt"])

        user_input = st.text_input("Your answer", key=key)

        correct_answer = step["answer"]
        user_answers.append(user_input)

        if user_input.strip() != "":
            if is_correct_answer(user_input, correct_answer):
                st.success("✅ Correct")
            else:
                st.error("❌ Try again")

        st.write("")

    st.session_state.scaffold_answer = user_answers
    return user_answers
