from src.agenteval import trace_handler
import pytest


@pytest.fixture
def trace_handler_fixture():
    return trace_handler.TraceHandler("TestTask")


class TestTraceHandler:

    def test_init(self, trace_handler_fixture):
        assert trace_handler_fixture.steps == []
        assert trace_handler_fixture.task_name == "TestTask"

    def test_add_step(self, trace_handler_fixture):

        trace_handler_fixture.add_step(step_name="test step", data="test data")

        step = trace_handler_fixture.steps[0]

        assert "timestamp" in step
        assert step["step_name"] == "test step"
        assert step["data"] == "test data"

    def test_add_step_without_name(self, trace_handler_fixture):

        trace_handler_fixture.add_step(data="test data")

        step = trace_handler_fixture.steps[0]

        assert step["step_name"] == self.test_add_step_without_name.__name__

    def test_dump_trace(self, tmp_path, trace_handler_fixture):
        trace_handler_fixture.trace_dir = tmp_path / "test_dir"

        trace_handler_fixture._dump_trace()

        assert (tmp_path / "test_dir" / "TestTask.json").exists()
