import streamlit as st
import pandas as pd
from core.db.client import get_supabase


_COLORSCALE = [
    [0.0, "#e74c3c"],
    [0.4, "#e67e22"],
    [0.7, "#27ae60"],
    [1.0, "#1e8449"],
]


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


def render_student_dashboard(user):
    st.header("My Progress")

    sb = get_supabase()
    uid = user["id"]

    try:
        attempts = sb.table("numeracy_attempts").select("*").eq("user_id", uid).execute().data
        tests = sb.table("numeracy_test_results").select("*").eq("user_id", uid).execute().data
    except Exception as e:
        st.error(f"Could not load data: {e}")
        return

    # ── Practice accuracy heatmap ──
    st.subheader("Practice Accuracy")
    if attempts:
        adf = pd.DataFrame(attempts)
        adf["pct"] = adf["correct"].astype(float) * 100
        topics = sorted(adf["topic"].unique())
        levels = sorted(adf["level"].unique())
        summary = adf.groupby(["topic", "level"])["pct"].mean().to_dict()
        st.plotly_chart(_heatmap(topics, levels, summary), use_container_width=True)
        st.caption("🟩 ≥ 70%   🟧 40–69%   🟥 < 40%   Grey = no attempts")
    else:
        st.info("No practice attempts yet. Generate some questions to see your accuracy here.")

    st.divider()

    # ── Test score heatmap ──
    st.subheader("Test Scores")
    if tests:
        tdf = pd.DataFrame(tests)
        tdf["pct"] = tdf["score"] / tdf["total"] * 100
        topics = sorted(tdf["topic"].unique())
        levels = sorted(tdf["level"].unique())
        summary = tdf.groupby(["topic", "level"])["pct"].mean().to_dict()
        st.plotly_chart(_heatmap(topics, levels, summary), use_container_width=True)
        st.caption("🟩 ≥ 70%   🟧 40–69%   🟥 < 40%   Grey = no tests taken")

        st.subheader("Recent Tests")
        recent = tdf.copy()
        recent["Topic"] = recent["topic"]
        recent["Level"] = "Level " + recent["level"].astype(str)
        recent["Score"] = recent["score"].astype(str) + " / " + recent["total"].astype(str)
        if "taken_at" in recent.columns:
            recent["Date"] = pd.to_datetime(recent["taken_at"]).dt.strftime("%d %b %Y %H:%M")
            recent = recent[["Date", "Topic", "Level", "Score"]].sort_values("Date", ascending=False)
        else:
            recent = recent[["Topic", "Level", "Score"]]
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.info("No tests taken yet. Complete a test to see your scores here.")
