import streamlit as st
import pandas as pd
from core.db.client import get_supabase
from core.auth.auth import reset_password


_COLORSCALE = [
    [0.0, "#e74c3c"],
    [0.4, "#e67e22"],
    [0.7, "#27ae60"],
    [1.0, "#1e8449"],
]


def _fetch_all():
    sb = get_supabase()
    users = (
        sb.table("users")
        .select("id,username,role,class_code,created_at")
        .eq("role", "student")
        .order("username")
        .execute().data
    )
    attempts = sb.table("numeracy_attempts").select("*").execute().data
    tests = sb.table("numeracy_test_results").select("*").execute().data
    return users, attempts, tests


def _heatmap(topics, levels, summary):
    import plotly.graph_objects as go
    level_labels = [f"Level {l}" for l in levels]
    z, annotations = [], []
    for r, topic in enumerate(topics):
        row = []
        for c, lvl in enumerate(levels):
            val = summary.get((topic, lvl))
            row.append(val)
            label = f"{val:.0f}%" if val is not None else ""
            annotations.append(dict(
                x=c, y=r, text=label, showarrow=False,
                font=dict(color="white", size=13),
            ))
        z.append(row)

    fig = go.Figure(go.Heatmap(
        z=z,
        x=level_labels,
        y=topics,
        colorscale=_COLORSCALE,
        zmin=0,
        zmax=100,
        showscale=False,
        hoverongaps=False,
        hovertemplate="%{y} — %{x}: %{z:.0f}%<extra></extra>",
    ))
    fig.update_layout(
        annotations=annotations,
        plot_bgcolor="#bdc3c7",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        height=max(160, len(topics) * 70 + 60),
        xaxis=dict(side="top", tickangle=-30),
        yaxis=dict(autorange="reversed"),
    )
    return fig


def render_dashboard():
    st.header("Teacher Dashboard")

    try:
        all_users, attempts, tests = _fetch_all()
    except Exception as e:
        st.error(f"Could not load data: {e}")
        return

    if not all_users:
        st.info("No students have signed up yet.")
        return

    # --- Class filter ---
    class_codes = sorted(set(u.get("class_code") or "" for u in all_users))
    class_codes = [c for c in class_codes if c]
    if class_codes:
        selected_class = st.selectbox(
            "Class", ["All classes"] + class_codes,
            label_visibility="collapsed", key="dashboard_class_filter",
        )
        st.caption(f"Showing: **{selected_class}**")
    else:
        selected_class = "All classes"

    users = (
        [u for u in all_users if (u.get("class_code") or "") == selected_class]
        if selected_class != "All classes"
        else all_users
    )

    user_ids = {u["id"] for u in users}
    filtered_attempts = [a for a in attempts if a["user_id"] in user_ids]
    filtered_tests = [t for t in tests if t["user_id"] in user_ids]

    # --- Overview metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Students", len(users))
    col2.metric("Total practice attempts", len(filtered_attempts))
    col3.metric("Total tests taken", len(filtered_tests))

    st.divider()

    # --- Summary table ---
    st.subheader("Student Overview")

    show_class_col = selected_class == "All classes" and bool(class_codes)
    rows = []
    for u in users:
        uid = u["id"]
        ua = [a for a in filtered_attempts if a["user_id"] == uid]
        ut = [t for t in filtered_tests if t["user_id"] == uid]
        n = len(ua)
        correct = sum(1 for a in ua if a["correct"])
        accuracy = f"{correct / n * 100:.0f}%" if n else "—"
        avg_score = (
            f"{sum(t['score'] for t in ut) / sum(t['total'] for t in ut) * 100:.0f}%"
            if ut else "—"
        )
        row = {"Student": u["username"]}
        if show_class_col:
            row["Class"] = u.get("class_code") or "—"
        row.update({
            "Practice attempts": n,
            "Accuracy": accuracy,
            "Tests taken": len(ut),
            "Avg test score": avg_score,
        })
        rows.append(row)

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()

    # --- Per-student drilldown ---
    st.subheader("Student Detail")
    selected = st.selectbox("Select student", [u["username"] for u in users])
    uid = next(u["id"] for u in users if u["username"] == selected)

    ua = [a for a in filtered_attempts if a["user_id"] == uid]
    ut = [t for t in filtered_tests if t["user_id"] == uid]

    col_a, col_t = st.columns(2)

    with col_a:
        st.markdown("**Practice attempts**")
        if ua:
            adf = pd.DataFrame(ua)
            summary = (
                adf.groupby(["topic", "level"])
                .agg(attempts=("correct", "count"), correct=("correct", "sum"))
                .reset_index()
            )
            summary["Accuracy"] = (
                (summary["correct"] / summary["attempts"] * 100)
                .round(0).astype(int).astype(str) + "%"
            )
            summary["Level"] = "Level " + summary["level"].astype(str)
            summary = summary.rename(columns={"topic": "Topic", "attempts": "Attempts"})[
                ["Topic", "Level", "Attempts", "Accuracy"]
            ]
            st.dataframe(summary, use_container_width=True, hide_index=True)
        else:
            st.info("No practice attempts yet.")

    with col_t:
        st.markdown("**Test results**")
        if ut:
            tdf = pd.DataFrame(ut)
            tdf["Score"] = tdf["score"].astype(str) + " / " + tdf["total"].astype(str)
            tdf["Level"] = "Level " + tdf["level"].astype(str)
            if "taken_at" in tdf.columns:
                tdf["Date"] = pd.to_datetime(tdf["taken_at"]).dt.strftime("%d %b %Y %H:%M")
                cols = ["Date", "Topic", "Level", "Score"]
            else:
                cols = ["Topic", "Level", "Score"]
            tdf = tdf.rename(columns={"topic": "Topic"})[cols]
            st.dataframe(tdf, use_container_width=True, hide_index=True)
        else:
            st.info("No tests taken yet.")

    st.divider()

    # --- Progress heatmap ---
    st.subheader("Progress Heatmap")
    if ua:
        adf = pd.DataFrame(ua)
        adf["pct"] = adf["correct"].astype(float) * 100
        topics = sorted(adf["topic"].unique())
        levels = sorted(adf["level"].unique())
        heat_summary = adf.groupby(["topic", "level"])["pct"].mean().to_dict()
        st.plotly_chart(_heatmap(topics, levels, heat_summary), use_container_width=True)
        st.caption("🟩 ≥ 70%   🟧 40–69%   🟥 < 40%   Grey = no data")
    else:
        st.info("No practice data to display.")

    st.divider()

    # --- Assign class code ---
    st.subheader("Assign Class Code")
    assign_student = st.selectbox("Student", [u["username"] for u in all_users], key="assign_select")
    assign_user = next(u for u in all_users if u["username"] == assign_student)
    current_code = assign_user.get("class_code") or ""
    with st.form("assign_class_form"):
        new_code = st.text_input("Class code", value=current_code, placeholder="e.g. 5A")
        submitted = st.form_submit_button("Save", type="primary")
    if submitted:
        try:
            code_to_save = new_code.strip().upper() or None
            get_supabase().table("users").update({"class_code": code_to_save}).eq("id", assign_user["id"]).execute()
            st.success(f"Class code for **{assign_student}** updated to **{code_to_save or '(none)'}**.")
            st.rerun()
        except Exception as e:
            st.error(f"Update failed: {e}")

    st.divider()

    # --- Password reset ---
    st.subheader("Reset Password")
    reset_student = st.selectbox("Student", [u["username"] for u in all_users], key="reset_select")
    with st.form("reset_password_form"):
        new_pw = st.text_input("New password", type="password")
        confirm_pw = st.text_input("Confirm new password", type="password")
        submitted = st.form_submit_button("Reset password", type="primary")
    if submitted:
        if not new_pw:
            st.error("Please enter a new password.")
        elif new_pw != confirm_pw:
            st.error("Passwords do not match.")
        elif len(new_pw) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            reset_uid = next(u["id"] for u in all_users if u["username"] == reset_student)
            error = reset_password(reset_uid, new_pw)
            if error:
                st.error(error)
            else:
                st.success(f"Password for **{reset_student}** has been reset.")
