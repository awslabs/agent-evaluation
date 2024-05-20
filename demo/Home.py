import os

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils.db_handling import create_table
from utils.state_handling import StateKeyEnum

st.set_page_config(
    layout="centered",
    page_title="Agent Evaluation",
    page_icon="⭐",
)

# set demo working directories
demo_work_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "workdir")
if not os.path.exists(demo_work_dir):
    os.mkdir(demo_work_dir)
if StateKeyEnum.DEMO_WORK_DIR not in st.session_state:
    st.session_state[StateKeyEnum.DEMO_WORK_DIR] = demo_work_dir
plan_dir = os.path.join(demo_work_dir, "plan")
if not os.path.exists(plan_dir):
    os.mkdir(plan_dir)
if StateKeyEnum.PLAN_DIR not in st.session_state:
    st.session_state[StateKeyEnum.PLAN_DIR] = plan_dir
plan_path = os.path.join(plan_dir, "agenteval.yml")
if StateKeyEnum.PLAN_PATH not in st.session_state:
    st.session_state[StateKeyEnum.PLAN_PATH] = plan_path
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
if not os.path.exists(static_file_dir):
    os.mkdir(static_file_dir)
result_dir = os.path.join(static_file_dir, "results")
if not os.path.exists(result_dir):
    os.mkdir(result_dir)
if StateKeyEnum.RESULT_DIR not in st.session_state:
    st.session_state[StateKeyEnum.RESULT_DIR] = result_dir

create_table()


@st.cache_data
def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("🥳")
st.title("Agent Evaluation!")

st.markdown(
    "Agent Evaluation is a LLM-powered framework for testing virtual agents."
    "Agent Evaluation implements an agent (Evaluator) that will orchestrate conversations with your agent (Target) and evaluate the responses during the conversation."
    "You simply define your test cases using natural language."
)

show = st.button("Start configuring your test plan!")
if show:
    switch_page("Configure test plan")

st.markdown(
    """
    Read more in the dedicated :balloon: [Agent Evaluation](https://github.com/awslabs/agent-evaluation/tree/main/docs).
    """
)
