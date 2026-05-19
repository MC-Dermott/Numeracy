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

# Track submission state
if "submitted" not in st.session_state:
    st.session_state.submitted = False

topic = st.selectbox(
    "Choose Topic",
    list(TOPIC_REGISTRY.keys())
)

selected_topic = TOPIC_REGISTRY[topic]
levels = selected_topic["levels"]

# Reset level when changing topic
if "last_topic" not in st.session_state:
    st.session_state.last_topic = topic

if st.session_state.last_topic != topic:
    st.session_state.selected_level = levels[0]["id"]
    st.session_state.last_topic = topic

# Initialise selected level
if "selected_level" not in st.session_state:
    st.session_state.selected_level = levels[0]["id"]

st.write("### Choose Level")

cols = st.columns(2)

for index, level_data in enumerate(levels):

    lvl_id = level_data["id"]

    button_text = (
        f"{level_data['label']}\n\n"
        f"{level_data['description']}"
    )

    button_type = (
        "primary"
        if st.session_state.selected_level == lvl_id
        else "secondary"
    )

    with cols[index % 2]:

        if st.button(
            button_text,
            key=f"btn_lvl_{topic}_{lvl_id}",
            type=button_type,
            use_container_width=True
        ):
            st.session_state.selected_level = lvl_id
            st.rerun()

level = st.session_state.selected_level


if st.button("Generate Question"):
    quiz["topic"] = topic
    quiz["level"] = level
    quiz["current_question"] = generate_question(topic, level)
    st.session_state.submitted = False
    st.rerun()

question = quiz.get("current_question")

if question:
    # 1. Top Core question interface (Suffix ensures unique widget keys)
    top_answer = render_question(question, suffix="top")

    # 2. Setup form submission button up top
    if st.button("Submit Answer", key="submit_top"):
        st.session_state.submitted = True

    # 3. Dynamic UI Based on State
    if st.session_state.submitted:
        # Check both locations. Use the scaffold answer if the top answer was left empty/0
        if isinstance(question.correct_answer, dict):
            if top_answer["hours"] == 0 and top_answer["minutes"] == 0 and "scaffold_answer" in st.session_state:
                user_answer = st.session_state.scaffold_answer
            else:
                user_answer = top_answer
                
            correct = user_answer == question.correct_answer
        else:
            if (top_answer == "" or top_answer == 0) and "scaffold_answer" in st.session_state:
                user_answer = st.session_state.scaffold_answer
            else:
                user_answer = top_answer
                
            correct = str(user_answer).strip() == str(question.correct_answer)

        if correct:
            st.success("✅ Correct")
        else:
            st.error(f"❌ Incorrect. Correct answer: {question.correct_answer}")

        # Always show worked solution after submitting
        render_solution(question)
    
    else:
        # Hide answers but offer clean, collapsible help blocks while working
        st.write("---")
        
        with st.expander("💡 Need Help? View Examples, Videos & Hints"):
            
            st.subheader("📝 Practice Examples")
            render_examples(question)
            
            st.subheader("🎥 Video Tutorial")
            render_videos(question)
            
            st.subheader("Scaffold")
            render_scaffold(question)
            
            st.write("---")
            st.subheader("✏️ Enter Your Final Answer Here")
            
            # Duplicate the answer boxes inside the scaffold area with a unique suffix
            scaffold_ans = render_question(question, suffix="scaffold")
            st.session_state.scaffold_answer = scaffold_ans
            
            if st.button("Submit Answer", key="submit_scaffold"):
                st.session_state.submitted = True
                st.rerun()

