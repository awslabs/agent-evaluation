import datetime
import os
import shutil
import threading
import time

import streamlit as st
import yaml
from streamlit_extras.switch_page_button import switch_page
from utils.db_handling import insert_result
from utils.state_handling import StateKeyEnum, check_state

from agenteval.plan import Plan
from agenteval.runner import Runner

# Check if all the paths were set if not go back to the Home page
check_state(st.session_state)
plan_dir = st.session_state[StateKeyEnum.PLAN_DIR]
plan_path = st.session_state[StateKeyEnum.PLAN_PATH]
result_dir = st.session_state[StateKeyEnum.RESULT_DIR]

# Load and display current test plan
try:
    with open(plan_path, "r") as f:
        plan_config = yaml.safe_load(f)
        st.json(plan_config)
        plan = Plan.load(plan_dir=plan_dir, filter=None)
except Exception as e:
    st.error(f"Failed to load plan: {e}")
    st.button("Reconfigure your test plan!")

if st.button("Run test"):
    # Make a working directory and run the test
    now = datetime.datetime.now()
    created_at = now.strftime("%Y-%m-%d %H:%M:%S")
    test_result_dir = os.path.join(result_dir, created_at)

    # Run the test
    runner = Runner(
        plan=plan,
        verbose=False,
        num_threads=None,
        work_dir=test_result_dir,
    )
    finished_at, status, test_passed_rate = None, None, None
    try:
        # Start the test in a separate thread 
        runner_thread = threading.Thread(target=runner.run)
        runner_thread.start()
        progress_bar = st.progress(0, text="Test is running ...")
        st.write(f"Starting {runner.num_tests} tests with max {runner.num_threads} workers.")
        start_time = datetime.datetime.now()
        num_completed = 0
        # Wait for the test to complete
        while num_completed < runner.num_tests:
            time.sleep(1)
            num_completed = len(list(filter(lambda x: x != None, runner.results.values())))
            percentage = num_completed / runner.num_tests
            progress_bar.progress(percentage, f'Progress: {percentage * 100} %')
        runner_thread.join()
        now = datetime.datetime.now()
        st.success(f"Test completed in {(now - start_time).total_seconds()} seconds")
        status = "completed"
        finished_at = now.strftime("%Y-%m-%d %H:%M:%S")
        test_passed_rate = (
            f"{runner.num_tests - runner.num_failed} / {runner.num_tests}"
        )
        with open(os.path.join(result_dir, created_at, "agenteval_summary.md")) as f:
            result = f.read()
            st.markdown(result, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Test failed: {e}")
        status = "error"
    finally:
        # copy test plan to the test result directory
        shutil.copy(plan_path, test_result_dir)
        # save the test result to the database
        insert_result(
            created_at, finished_at, plan_config["target"]["type"], status, test_passed_rate
        )

if st.button("Manage all results"):
    switch_page("Manage result")
