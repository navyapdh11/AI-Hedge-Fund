import sys
import os
import pytest
from hypothesis import given, strategies as st

# Setup path to include agents
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../agents"))
sys.path.append(os.path.join(current_dir, "../agents/trading"))

from portfolio_manager import decide_trade

@given(st.floats(min_value=0.0, max_value=1.0), st.sampled_from(["NORMAL", "CRISIS"]))
def test_portfolio_manager_trade_logic(consensus, regime):
    decision = decide_trade(consensus, regime)
    assert decision in ["EXECUTE_TRADE", "HOLD"]
    if regime == "CRISIS":
        assert decision == "HOLD"
