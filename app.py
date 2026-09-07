import json
import streamlit as st
from analyzer import analyze_week, extract_docx_text

st.set_page_config(page_title="AI Weekly Performance Coach", page_icon="🎯", layout="wide")
st.title("🎯 AI Weekly Performance Coach")
st.caption("Audit your past week and turn the lessons into a realistic plan for the next week.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Groq API key", type="password")
    st.info("Best input format: Task — time spent — status")

left, right = st.columns(2)

with left:
    st.subheader("1. Past Week")
    weekly_text = st.text_area(
        "Paste weekly activities / to-do record",
        height=360,
        placeholder="Monday\nThesis research — 2 hours — completed\nInstagram — 1 hour\nGym — 1 hour — completed"
    )

with right:
    st.subheader("2. Weekly Goals")
    goals_text = st.text_area(
        "What did you plan or want to achieve?",
        height=170,
        placeholder="Complete 10 hours thesis work\nLearn Python for 5 hours\nGym 4 times"
    )
    st.subheader("3. Optional DOCX")
    uploaded = st.file_uploader("Upload weekly record", type=["docx"])
    if uploaded:
        try:
            doc_text = extract_docx_text(uploaded)
            if doc_text.strip():
                weekly_text = (weekly_text.strip() + "\n\n" + doc_text.strip()).strip()
                st.success("DOCX extracted successfully.")
            else:
                st.warning("No readable text found in DOCX.")
        except Exception as e:
            st.error(f"Could not read DOCX: {e}")

st.divider()

if st.button("🔍 Audit My Week", type="primary", use_container_width=True):
    if not weekly_text.strip():
        st.error("Please paste weekly activities or upload a DOCX.")
        st.stop()
    with st.spinner("Analyzing your week..."):
        try:
            st.session_state.result = analyze_week(weekly_text, goals_text, api_key or None)
        except Exception as e:
            st.error(str(e))
            st.stop()

result = st.session_state.get("result")
if result:
    analysis = result["weekly_analysis"]
    st.header("Your Weekly Audit")
    c1, c2 = st.columns([1, 3])
    c1.metric("Overall Score", f'{analysis["overall_score"]}/100')
    c2.write(analysis["summary"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tracked Time", f'{analysis["total_tracked_hours"]:.1f} h')
    m2.metric("High-Impact", f'{analysis["high_impact_hours"]:.1f} h')
    m3.metric("Low-Value", f'{analysis["low_value_hours"]:.1f} h')
    m4.metric("Goal Progress", f'{analysis["goal_completion_percent"]:.0f}%')

    tabs = st.tabs(["⏱️ Time Saved", "🐌 Time Eaters", "📊 Weekly Audit",
                    "🔄 Keep Going / Good / Best", "🔮 Next Week", "🏆 Final Result"])

    with tabs[0]:
        x = result["time_saved"]
        st.metric("Potential recovery", f'{x["potentially_recoverable_hours"]:.1f} hours')
        st.write(x["explanation"])
        for item in x["actions"]:
            st.write("• " + item)

    with tabs[1]:
        for item in result["time_eaters"]:
            st.markdown(f'### {item["activity"]}')
            a, b = st.columns(2)
            a.write(f'**Time:** {item["hours"]:.1f} h')
            b.write(f'**Severity:** {item["severity"]}')
            st.write(item["why"])
            if item["suggestion"]:
                st.write(f'**Suggestion:** {item["suggestion"]}')

    with tabs[2]:
        x = result["weekly_audit"]
        st.write(f'**Strength:** {x["strength"]}')
        st.write(f'**Main weakness:** {x["main_weakness"]}')
        st.write(f'**Goal result:** {x["goal_result"]}')
        for item in x["key_observations"]:
            st.write("• " + item)

    with tabs[3]:
        x = result["weekly_audit"]["categories"]
        for title, key in [("🟢 Keep Going", "keep_going"), ("🟡 Good", "good"), ("🔵 Best", "best")]:
            st.subheader(title)
            for item in x[key]:
                st.write("• " + item)

    with tabs[4]:
        x = result["next_week_plan"]
        st.subheader("🎯 Top 3 Priorities")
        for i, item in enumerate(x["top_priorities"], 1):
            st.write(f"**{i}.** {item}")
        st.subheader("⏰ Suggested Time Allocation")
        for item in x["time_allocation"]:
            st.write("• " + item)
        a, b = st.columns(2)
        with a:
            st.subheader("🔄 Keep")
            for item in x["keep"]:
                st.write("• " + item)
        with b:
            st.subheader("🚫 Reduce")
            for item in x["reduce"]:
                st.write("• " + item)
        st.success(x["one_most_important_change"])

    with tabs[5]:
        x = result["final_result"]
        st.subheader(x["headline"])
        st.write(x["verdict"])
        st.write(f'**Biggest win:** {x["biggest_win"]}')
        st.write(f'**Biggest problem:** {x["biggest_problem"]}')
        st.write(f'**Potential time recovery:** {x["potential_time_recovery_hours"]:.1f} hours')
        st.subheader("Next week's 3 actions")
        for i, item in enumerate(x["next_week_actions"], 1):
            st.write(f"**{i}.** {item}")
        with st.expander("View structured JSON"):
            st.json(result)
            st.download_button(
                "Download JSON",
                json.dumps(result, indent=2, ensure_ascii=False),
                "weekly_audit.json",
                "application/json"
            )
