import streamlit as st

from core.engine.session_manager import initialise_session
from core.engine.question_factory import generate_question, TOPIC_REGISTRY
from core.ui.question_ui import render_question
from core.ui.examples_ui import render_examples
from core.ui.scaffold_ui import render_scaffold
from core.ui.solution_ui import render_solution

initialise_session()

st.set_page_config(page_title="Maths Learning Platform")
st.title("📘 Maths Learning Platform")

quiz = st.session_state.quiz

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ─── MODE SELECTION ──────────────────────────────────────────────
mode = st.radio("Mode", ["Practice", "Test"], horizontal=True, label_visibility="collapsed")

if quiz.get("mode") != mode:
    quiz["mode"] = mode
    quiz["current_question"] = None
    st.session_state.submitted = False
    if mode == "Test":
        quiz["test_question_num"] = 0
        quiz["test_score"] = 0
        quiz["test_complete"] = False
    st.rerun()

# ─── TOPIC & LEVEL SELECTION (shown when not mid-test) ───────────
test_in_progress = (
    mode == "Test"
    and quiz.get("test_question_num", 0) > 0
    and not quiz.get("test_complete")
)

if test_in_progress:
    st.info(f"Test in progress: **{quiz['topic']}** | **Level {quiz['level']}**")
else:
    topic = st.selectbox("Choose Topic", list(TOPIC_REGISTRY.keys()))
    selected_topic = TOPIC_REGISTRY[topic]
    levels = selected_topic["levels"]

    if "last_topic" not in st.session_state:
        st.session_state.last_topic = topic

    if st.session_state.last_topic != topic:
        st.session_state.selected_level = levels[0]["id"]
        st.session_state.last_topic = topic

    if "selected_level" not in st.session_state:
        st.session_state.selected_level = levels[0]["id"]

    st.write("### Choose Level")
    cols = st.columns(2)

    for index, level_data in enumerate(levels):
        lvl_id = level_data["id"]
        button_text = f"{level_data['label']}\n\n{level_data['description']}"
        button_type = "primary" if st.session_state.selected_level == lvl_id else "secondary"
        with cols[index % 2]:
            if st.button(button_text, key=f"btn_lvl_{topic}_{lvl_id}", type=button_type, use_container_width=True):
                st.session_state.selected_level = lvl_id
                st.rerun()

    level = st.session_state.selected_level


# ─── PRACTICE MODE ───────────────────────────────────────────────
if mode == "Practice":
    if st.button("Generate Question"):
        quiz["topic"] = topic
        quiz["level"] = level
        quiz["current_question"] = generate_question(topic, level)
        st.session_state.submitted = False
        st.rerun()

    question = quiz.get("current_question")

    if question:
        top_answer = render_question(question, suffix="top")

        if st.button("Submit Answer", key="submit_top"):
            st.session_state.submitted = True

        if st.session_state.submitted:
            if isinstance(question.correct_answer, dict):
                correct = top_answer == question.correct_answer
            else:
                correct = str(top_answer).strip() == str(question.correct_answer)

            if correct:
                st.success("✅ Correct")
            else:
                st.error(f"❌ Incorrect. Correct answer: {question.correct_answer}")

            render_solution(question)

        else:
            st.write("---")
            with st.expander("📝 Examples"):
                render_examples(question)
            with st.expander("💡 Scaffold"):
                render_scaffold(question)


# ─── TEST MODE ───────────────────────────────────────────────────
else:
    TEST_LENGTH = 5

    # ── Results screen ──
    if quiz.get("test_complete"):
        score = quiz["test_score"]
        st.markdown("---")
        st.markdown("## Test Complete!")
        st.markdown(f"### Your Score: {score} / {TEST_LENGTH}")

        if score == TEST_LENGTH:
            st.success("Perfect score! Outstanding work!")
        elif score >= 4:
            st.success("Excellent work!")
        elif score >= 3:
            st.info("Good effort! Keep practising.")
        else:
            st.warning("Keep practising — you'll get there!")

        if st.button("Try Again", type="primary"):
            quiz["test_question_num"] = 0
            quiz["test_score"] = 0
            quiz["test_complete"] = False
            quiz["current_question"] = None
            st.session_state.submitted = False
            st.rerun()

    # ── Start screen ──
    elif quiz.get("test_question_num", 0) == 0:
        st.info("Select a topic and level above, then click **Start Test** to begin 5 questions.")
        if st.button("Start Test", type="primary"):
            quiz["topic"] = topic
            quiz["level"] = level
            quiz["test_question_num"] = 1
            quiz["test_score"] = 0
            quiz["test_complete"] = False
            quiz["current_question"] = generate_question(topic, level)
            st.session_state.submitted = False
            st.rerun()

    # ── Question screen ──
    else:
        test_q_num = quiz["test_question_num"]
        test_score = quiz["test_score"]

        col1, col2 = st.columns([4, 1])
        with col1:
            st.progress(test_q_num / TEST_LENGTH)
        with col2:
            st.markdown(f"**{test_q_num} / {TEST_LENGTH}** &nbsp; ⭐ {test_score}")

        question = quiz["current_question"]
        top_answer = render_question(question, suffix="top")

        if not st.session_state.submitted:
            if st.button("Submit Answer", key="submit_test"):
                if isinstance(question.correct_answer, dict):
                    correct = top_answer == question.correct_answer
                else:
                    correct = str(top_answer).strip() == str(question.correct_answer)

                st.session_state.test_correct = correct
                if correct:
                    quiz["test_score"] += 1

                st.session_state.submitted = True
                st.rerun()
        else:
            correct = st.session_state.get("test_correct", False)

            if correct:
                st.success("✅ Correct")
            else:
                st.error(f"❌ Incorrect. Correct answer: {question.correct_answer}")

            render_solution(question)

            if test_q_num < TEST_LENGTH:
                if st.button("Next Question", type="primary"):
                    quiz["test_question_num"] += 1
                    quiz["current_question"] = generate_question(quiz["topic"], quiz["level"])
                    st.session_state.submitted = False
                    st.rerun()
            else:
                if st.button("See Results", type="primary"):
                    quiz["test_complete"] = True
                    st.rerun()
