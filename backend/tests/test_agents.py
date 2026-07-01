from app.agents.copy_agent import CopyAgent
from app.agents.segment_agent import SegmentAgent

def test_copy_agent_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    agent = CopyAgent()
    assert agent.client is None

    result = agent.generate_copy({"product": "TestPlatform"}, "friendly")
    assert "channel" in result
    assert result["tone"] == "friendly"
    assert len(result["variants"]) == 2
    assert "Hey there! 👋" in result["variants"][0]["body"]

def test_segment_agent_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    agent = SegmentAgent()
    assert agent.client is None

    result = agent.generate_audience("activation")
    assert "name" in result
    assert result["name"] == "Users needing activation"
    assert "definition" in result
    assert "include" in result["definition"]
