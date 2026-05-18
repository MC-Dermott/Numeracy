
import streamlit as st

def render_examples(question):

    if not question.examples:
        return

    with st.expander("📚 Example"):

        for example in question.examples:
            st.markdown(f"- {example}")
