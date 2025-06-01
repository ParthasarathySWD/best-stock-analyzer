import os
import aiohttp
import pandas as pd
import requests
import json

from datetime import datetime, timedelta
from dotenv import load_dotenv
import yfinance as yf
load_dotenv()


class MarketData:
    """Handles all market data fetching operations."""

    def __init__(self):
        self.api_key = os.getenv("TIINGO_API_KEY")
        if not self.api_key:
            raise ValueError("TIINGO_API_KEY not found in environment")

        self.headers = {"Content-Type": "application/json", "Authorization": f"Token {self.api_key}"}

    async def get_historical_data(self, symbol: str, lookback_days: int = 365) -> pd.DataFrame:
        """
        Fetch historical daily data for a given symbol.

        Args:
            symbol (str): The stock symbol to fetch data for.
            lookback_days (int): Number of days to look back from today.

        Returns:
            pd.DataFrame: DataFrame containing historical market data.

        Raises:
            ValueError: If the symbol is invalid or no data is returned.
            Exception: For other unexpected issues during the fetch operation.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)

        try:
            # Determine the correct yfinance symbol
            yf_symbol = symbol
            if not (symbol.endswith('.NS') or symbol.endswith('.BO')):
                # Try NSE first, fallback to BSE if NSE fails
                df = yf.download(f"{symbol}.NS", start=start_date, end=end_date, auto_adjust=False)
                if df.empty:
                    df = yf.download(f"{symbol}.BO", start=start_date, end=end_date, auto_adjust=False)
                    yf_symbol = f"{symbol}.BO"
                else:
                    yf_symbol = f"{symbol}.NS"
            else:
                df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=False)
                yf_symbol = symbol

            json_str = self.yfinance_to_tiingo_json(df, symbol)
            with open("yfinance_tiingo_format.json", "w") as f:
                f.write(json_str)

            if df.empty:
                raise ValueError(f"No data returned for {symbol}")
            
            df = pd.read_json(json_str)
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
            df["symbol"] = symbol.upper()
            return df

        except aiohttp.ClientError as e:
            raise ConnectionError(f"Network error while fetching data for {symbol}: {e}")
        except ValueError as ve:
            raise ve  # Propagate value errors (symbol issues, no data, etc.)
        except Exception as e:
            raise Exception(f"Unexpected error fetching data for {symbol}: {e}")



    def yfinance_to_tiingo_json(self, df: pd.DataFrame, symbol: str) -> str:
        df = df.reset_index()

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join([str(i) for i in col if i]) for col in df.columns.values]

        # Remove symbol prefix if present (e.g., 'Open_AAPL' -> 'Open')
        df.columns = [col.replace(f"_{symbol}", "") for col in df.columns]

        # Rename columns to match target
        df = df.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adjClose",
            "Volume": "volume"
        })

        # Add missing columns with default values if not present
        for col in ["adjOpen", "adjHigh", "adjLow", "adjVolume", "divCash", "splitFactor"]:
            if col not in df.columns:
                df[col] = 0.0 if col != "splitFactor" else 1.0

        # Fill adjusted columns with actual or fallback values
        df["adjOpen"] = df["open"]
        df["adjHigh"] = df["high"]
        df["adjLow"] = df["low"]
        df["adjVolume"] = df["volume"]

        # Format date as ISO string
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%dT00:00:00.000Z")

        # Select and order columns as in your example
        columns = [
            "date", "close", "high", "low", "open", "volume",
            "adjClose", "adjHigh", "adjLow", "adjOpen", "adjVolume",
            "divCash", "splitFactor"
        ]
        records = df[columns].to_dict(orient="records")
        return json.dumps(records, ensure_ascii=False, indent=2)
    
# md = MarketData()
# end_date = datetime.now()
# start_date = end_date - timedelta(days=365)
# symbol = "AAPL"
# df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=False)
# print(md.yfinance_to_tiingo_json(df, symbol))