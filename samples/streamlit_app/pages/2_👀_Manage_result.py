import os
import shutil

import streamlit as st
from utils.db_handling import delete_results, get_results
from utils.state_handling import StateKeyEnum, check_state

check_state(st.session_state)
result_dir = st.session_state[StateKeyEnum.RESULT_DIR]

st.cache_data.clear()
results = get_results()
if results is None or results.empty:
    st.warning("No results found")


else:
    st.info("Review the results", icon="ℹ️")
    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True,
    )

    test_id_1 = st.number_input(
        "Select test id",
        min_value=results["id"].min(),
        max_value=results["id"].max(),
        value="min",
    )

    selected_test_1 = results.loc[results["id"] == test_id_1]["created_at"].values[0]
    test_1_result_path = os.path.join(
        result_dir, selected_test_1, "agenteval_summary.md"
    )
    test_1_plan_path = os.path.join(result_dir, selected_test_1, "agenteval.yml")
    trace_1_path = os.path.join(result_dir, selected_test_1, "agenteval_traces")

    if st.button("Show result"):
        with st.expander(f"View test {test_id_1} plan"):
            with open(test_1_plan_path) as f:
                st.code(f.read(), language="yaml")
        with st.expander(f"View test {test_id_1} result summary"):
            with open(test_1_result_path) as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        with st.expander(f"View test {test_id_1} traces"):
            for filename in os.listdir(trace_1_path):
                st.link_button(
                    filename,
                    f"http://localhost:8501/app/static/results/{selected_test_1}/agenteval_traces/{filename}",
                )

    if st.button("Delete result"):
        delete_results(test_id_1)
        shutil.rmtree(os.path.join(result_dir, selected_test_1))
        st.success("Test result deleted")
