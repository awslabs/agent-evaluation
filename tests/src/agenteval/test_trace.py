from src.agenteval import trace
import pytest
import datetime


@pytest.fixture
def trace_fixture():
    return trace.Trace()


class TestTrace:
    def test_add_event(self, trace_fixture):
        trace_fixture.add_event(data={})

        event = trace_fixture.events[0]

        assert event["name"] == self.test_add_event.__name__
        assert event["data"] == {}
        assert isinstance(event["timestamp"], datetime.datetime)
