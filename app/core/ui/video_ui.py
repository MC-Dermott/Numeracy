
import streamlit as st

def render_videos(question):

    if not question.videos:
        return

    with st.expander("🎥 Video Tutorial"):

        for video in question.videos:

            st.markdown(
                f"- [{video['title']}]({video['url']})"
            )
