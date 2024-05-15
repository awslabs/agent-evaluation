import io
import os

import streamlit as st
import yaml
from streamlit_extras.switch_page_button import switch_page
from utils.state_handling import StateKeyEnum, check_state

from agenteval.plan import _INIT_PLAN

# Check if all the paths were set if not go back to the Home page
check_state(st.session_state)
plan_path = st.session_state[StateKeyEnum.PLAN_PATH]

# Show existing test plan if it exists
string_data = None
if os.path.exists(plan_path):
    with open(plan_path, "r") as f:
        string_data = f.read()
else:
    string_data = yaml.dump(_INIT_PLAN)

st.info(
    "Configure your test plan by uploading an existing plan or creating from scatch in the text area.",
    icon="ℹ️",
)
current_plan = st.file_uploader("Upload", type=["yaml", "yml"])

if current_plan:
    # read the file
    bytes_data = current_plan.getvalue()
    stringio = io.StringIO(current_plan.getvalue().decode("utf-8"))
    # To read file as string:
    string_data = stringio.read()

# Allow editing on the test plan
txt = st.text_area(label="Text plan", value=string_data, height=200)

st.info("Review your plan and save it.", icon="ℹ️")
loaded_config = yaml.safe_load(txt)
try:
    st.json(loaded_config)
except Exception as e:
    st.error("Invalid YAML format")

if st.button("Save"):
    st.write(plan_path)
    with open(plan_path, "w") as f:
        yaml.dump(loaded_config, f)
    st.success(f"Test plan saved to {plan_path}", icon="✅")

if st.button("Advance to next page to run your test!"):
    switch_page("Run test plan")
