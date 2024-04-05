from src.agenteval import trace_handler
import pytest


@pytest.fixture
def trace_handler_fixture():
    return trace_handler.TraceHandler("my_test", "test_dir")


class TestTraceHandler:

    def test_init(self, trace_handler_fixture):
        assert trace_handler_fixture.steps == []
        assert trace_handler_fixture.test_name == "my_test"
        assert trace_handler_fixture.start_time is None
        assert trace_handler_fixture.end_time is None

    def test_enter(self, mocker, trace_handler_fixture):

        mock_dump_trace = mocker.patch.object(trace_handler_fixture, "_dump_trace")

        with trace_handler_fixture:
            pass

        assert isinstance(trace_handler_fixture.start_time, trace_handler.datetime)
        assert isinstance(trace_handler_fixture.end_time, trace_handler.datetime)

        mock_dump_trace.assert_called_once()

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

        assert (tmp_path / "test_dir" / "my_test.json").exists()
