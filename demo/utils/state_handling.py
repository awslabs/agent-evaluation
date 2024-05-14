from enum import StrEnum

from streamlit_extras.switch_page_button import switch_page


class StateKeyEnum(StrEnum):
    """
    State keys for storing session state across pages
    """

    # Plan
    PLAN_DIR = "plan_dir"
    PLAN_PATH = "plan_path"
    RESULT_DIR = "result_dir"
    # Demo work direcotry
    DEMO_WORK_DIR = "demo_work_dir"


def check_state(session_state: object) -> None:
    """
    Check if the session state is valid. If not, switch to the home page.
    """
    # Check if all the required session state keys are set. If not, switch to the home page.
    for key in StateKeyEnum:
        if key not in session_state:
            switch_page("Home")
            return