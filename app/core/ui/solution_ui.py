
import streamlit as st

def render_solution(question):

   # with st.expander("✅ Worked Solution"):

        for step in question.worked_solution:
            st.markdown(f"- {step}")
