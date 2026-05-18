
import streamlit as st

def render_scaffold(question):

    responses = []

    if not question.scaffold_steps:
        return responses

    with st.expander("🧩 Scaffold Support"):

        for idx, step in enumerate(question.scaffold_steps):

            st.markdown(f"### Step {idx + 1}")

            response = st.text_input(
                step,
                key=f"scaffold_{idx}"
            )

            responses.append(response)

    return responses
