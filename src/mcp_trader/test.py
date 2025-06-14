from mcp_trader.data import MarketData
from mcp_trader.indicators import FundamentalAnalysis
import asyncio
import asyncio
import traceback
import json
import pandas as pd

# mdata = MarketData()
# fa = FundamentalAnalysis()
# print("MarketData and FundamentalAnalysis classes imported successfully.")

# stock_financial_data = mdata.get_fundamental_data("ITC.NS")
# # Example usage of MarketData and FundamentalAnalysis classes
# key_financial_data = fa.fetch_fundamental_data(stock_financial_data)

# print("Key financial data extracted successfully:", key_financial_data)
# # Example usage of MarketData and FundamentalAnalysis classes

async def analyze_fundamental_data(symbol: str) -> str:
    """Asynchronously fetch and analyze fundamental data for a given stock symbol."""
    market_data = MarketData()
    fund_analysis = FundamentalAnalysis()

    data = await market_data.get_fundamental_data(symbol)
    if not data and "status" in data and data["status"] == "error":
        raise ValueError(f"Error fetching fundamental data: {data.get('error', 'Unknown error')}")

    key_financial_data = fund_analysis.extract_key_financial_data(data)

    analysis = f"""
Fundamental Analysis for {symbol}:

Key financial ratios:
"""

    for key, value in key_financial_data["ratios"].items():
        if isinstance(value, (int, float)) and pd.isna(value):
            continue  # Skip NaN values
        analysis += f"- {key}: {value}\n"

    analysis += f"""
    Latest financials:
    """

    for key, value in key_financial_data["statistics"].items():
        if isinstance(value, (int, float)) and pd.isna(value):
            continue  # Skip NaN values
        analysis += f"- {key}: {value}\n"

    analysis += f"""
    Total Revenue by Year:
    """

    for year, value in key_financial_data["results"]["Total Revenue"].items():
        if isinstance(value, (int, float)) and pd.isna(value):
            continue  # Skip NaN values
        analysis += f"- {year}: {value}\n"

    analysis += f"""
    Net Income (in billions):
    """

    for year, value in key_financial_data["results"]["Net Income"].items():
        if isinstance(value, (int, float)) and pd.isna(value):
            continue  # Skip NaN values
        analysis += f"- {year}: {value}\n"
    # print(analysis)
    return analysis

if __name__ == "__main__":
    symbol = "ITC.NS"  # Example stock symbol
    loop = asyncio.get_event_loop()
    analysis_result = loop.run_until_complete(analyze_fundamental_data(symbol))
    print(analysis_result)