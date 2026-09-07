tabs = st.tabs(["⏱️ Time Saved", "🐌 Time Eaters", "📊 Weekly Audit",
                    "🔄 Keep Going / Good / Best", "🔮 Next Week", "🏆 Final Result"])

    with tabs[0]:
        x = result["time_saved"]
        st.metric("Potential recovery", f'{x["potentially_recoverable_hours"]:.1f} hours')
        st.write(x["explanation"])
        for item in x["actions"]:
            st.write("• " + _safe_item(item))

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
            st.write("• " + _safe_item(item))

    with tabs[3]:
        x = result["weekly_audit"]["categories"]
        for title, key in [("🟢 Keep Going", "keep_going"), ("🟡 Good", "good"), ("🔵 Best", "best")]:
            st.subheader(title)
            for item in x[key]:
                st.write("• " + _safe_item(item))

    with tabs[4]:
        x = result["next_week_plan"]
        st.subheader("🎯 Top 3 Priorities")
        for i, item in enumerate(x["top_priorities"], 1):
            st.write(f"**{i}.** {_safe_item(item)}")
        st.subheader("⏰ Suggested Time Allocation")
        for item in x["time_allocation"]:
            st.write("• " + _safe_item(item))
        a, b = st.columns(2)
        with a:
            st.subheader("🔄 Keep")
            for item in x["keep"]:
                st.write("• " + _safe_item(item))
        with b:
            st.subheader("🚫 Reduce")
            for item in x["reduce"]:
                st.write("• " + _safe_item(item))
        st.success(_safe_item(x["one_most_important_change"]))

    with tabs[5]:
        x = result["final_result"]
        st.subheader(x["headline"])
        st.write(x["verdict"])
        st.write(f'**Biggest win:** {x["biggest_win"]}')
        st.write(f'**Biggest problem:** {x["biggest_problem"]}')
        st.write(f'**Potential time recovery:** {x["potential_time_recovery_hours"]:.1f} hours')
        st.subheader("Next week's 3 actions")
        for i, item in enumerate(x["next_week_actions"], 1):
            st.write(f"**{i}.** {_safe_item(item)}")
        with st.expander("View structured JSON"):
            st.json(result)
            st.download_button(
                "Download JSON",
                json.dumps(result, indent=2, ensure_ascii=False),
                "weekly_audit.json",
                "application/json"
            )
