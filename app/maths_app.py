import streamlit as st

from core.engine.session_manager import initialise_session
from core.engine.question_factory import generate_question, TOPIC_REGISTRY
from core.ui.question_ui import render_question
from core.ui.scaffold_ui import render_scaffold
from core.ui.solution_ui import render_solution
from core.ui.auth_ui import render_auth
from core.ui.dashboard_ui import render_dashboard
from core.ui.student_dashboard_ui import render_student_dashboard
from core.db.tracker import save_practice_attempt, save_test_result

initialise_session()

st.set_page_config(page_title="Maths Learning Platform")

if "submitted" not in st.session_state:
    st.session_state.submitted = False


def _check_answer(user_answer, question) -> bool:
    if isinstance(question.correct_answer, dict):
        return user_answer == question.correct_answer
    accepted = question.metadata.get("accepted_answers") if question.metadata else None
    if accepted:
        normalized = (
            str(user_answer).strip().lower()
            .replace("²", "2").replace("^2", "2").replace(" ", "")
        )
        return normalized in accepted
    return str(user_answer).strip() == str(question.correct_answer)


def _do_logout():
    for key in ["user", "submitted", "last_tracked_qid", "show_dashboard", "show_student_dashboard"]:
        st.session_state.pop(key, None)
    quiz = st.session_state.get("quiz", {})
    quiz["current_question"] = None
    quiz["mode"] = None
    quiz["test_question_num"] = 0
    quiz["test_score"] = 0
    quiz["test_complete"] = False


def _render_auth_button():
    user = st.session_state.get("user")
    if user:
        st.caption(f"**{user['username']}**")
        if st.button("Log out", key="logout_corner"):
            _do_logout()
            st.rerun()
    else:
        if st.button("Log in / Sign up", key="login_corner"):
            st.session_state.show_auth = True
            st.rerun()


# --- Auth page ---
if st.session_state.get("show_auth"):
    if st.button("← Back"):
        st.session_state.pop("show_auth", None)
        st.rerun()
    render_auth()
    st.stop()

user = st.session_state.get("user")

# --- Login gate: block all access until authenticated ---
if not user:
    render_auth()
    st.stop()

user_id = user["id"] if user else None

# --- Student progress dashboard ---
if st.session_state.get("show_student_dashboard"):
    st.title("Maths Learning Platform")
    col_back, col_corner = st.columns([5, 1])
    with col_back:
        if st.button("← Back to practice"):
            st.session_state.pop("show_student_dashboard", None)
            st.rerun()
    with col_corner:
        _render_auth_button()
    render_student_dashboard(user)
    st.stop()

# --- Teacher dashboard ---
if st.session_state.get("show_dashboard"):
    st.title("Maths Learning Platform")
    col_back, col_corner = st.columns([5, 1])
    with col_back:
        if st.button("← Back to practice"):
            st.session_state.pop("show_dashboard", None)
            st.rerun()
    with col_corner:
        _render_auth_button()
    render_dashboard()
    st.stop()

# --- Title row ---
col_title, col_corner = st.columns([5, 1])
with col_title:
    st.title("Maths Learning Platform")
with col_corner:
    st.write("")
    _render_auth_button()

if user and user.get("role") == "teacher":
    if st.button("📊 Teacher Dashboard", use_container_width=True):
        st.session_state.show_dashboard = True
        st.rerun()
    st.write("")

if st.button("📈 My Progress", use_container_width=True):
    st.session_state.show_student_dashboard = True
    st.rerun()
st.write("")

quiz = st.session_state.quiz

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
        st.session_state.pop("last_tracked_qid", None)
        st.rerun()

    question = quiz.get("current_question")

    if question:
        top_answer = render_question(question, suffix="top")

        if st.button("Submit Answer", key="submit_top"):
            st.session_state.submitted = True

        if st.session_state.submitted:
            correct = _check_answer(top_answer, question)

            if user_id and st.session_state.get("last_tracked_qid") != question.qid:
                save_practice_attempt(user_id, quiz["topic"], quiz["level"], correct)
                st.session_state.last_tracked_qid = question.qid

            if correct:
                st.success("✅ Correct")
            else:
                st.error(f"❌ Incorrect. Correct answer: {question.correct_answer}")

            render_solution(question)

        else:
            st.write("---")
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
                correct = _check_answer(top_answer, question)

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
                    if user_id:
                        save_test_result(user_id, quiz["topic"], quiz["level"], quiz["test_score"], TEST_LENGTH)
                    st.rerun()
