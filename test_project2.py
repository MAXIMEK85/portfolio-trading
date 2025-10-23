from project import calculate_ma, determine_trends, get_stock_data
import pytest
import pandas as pd

def test_calculate_ma():
    data = pd.DataFrame({"Close": [10, 20, 30, 40, 50]})
    result = calculate_ma(data, 3)

    assert "MA_3" in result.columns
    assert pd.isna(result["MA_3"].iloc[0])
    assert result["MA_3"].iloc[-1] == pytest.approx((30 + 40 + 50)/3)

def test_determine_trends():
    data = pd.DataFrame({
        "Close": [100, 110, 120, 130, 140],
        "MA_50": [90, 95, 100, 105, 110],
        "MA_200": [80, 85, 90, 95, 100]
    })
    result = determine_trends(data)
    assert result["short_term"] == "short-term bullish"
    assert result["long_term"] == "long-term bullish"

def test_get_stock_data():
    data = get_stock_data("AAPL", period="1y")
    assert not data.empty
    assert "Close" in data.columns


