import pandas as pd
import pandas_ta as ta
import numpy as np

from typing import Dict, Any, List
from .utils import DataUtils
class FundamentalAnalysis:
    """Placeholder for fundamental analysis tools."""
    
    @staticmethod
    def extract_key_financial_data(data: dict) -> Dict[str, Any]:
        """
        Fetch fundamental data for a given stock symbol.
        
        Args:
            symbol (str): The stock symbol to fetch data for.
        
        Returns:
            Dict[str, Any]: Fundamental data dictionary.
        """
        # Placeholder implementation
        try:
            # Get historical market data (e.g., last 5 years)
            hist_data = data['hist_data']
            if hist_data.empty:
                current_price = None
            else:
                current_price = hist_data['Close'].iloc[-1]
                

            # Get income statement
            income_statement = data['income_statement']
            if income_statement.empty:
                income_statement_t = None;
            else:
                income_statement_t = income_statement.T.sort_index()
                

            # Get balance sheet
            balance_sheet = data['balance_sheet']
            if balance_sheet.empty:
                balance_sheet_t = None;
            else:
                balance_sheet_t = balance_sheet.T.sort_index()
                

            # Get cash flow statement
            cash_flow = data['cash_flow']
            if cash_flow.empty:
                cash_flow_t = None;
            else:
                cash_flow_t = cash_flow.T.sort_index()
                

            # Get key statistics and company info
            info = data['info']

        except Exception as e:
            return {
                "status": "error", 
                "error": f"Error during data collection: {e}"
            }

        try:

            ratios = {}
            statistics = {}
            results = {}
            if info:
                display_info_keys = ['marketCap', 'trailingPE', 'forwardPE', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'industry', 'sector', 'sharesOutstanding', 'trailingEps']
                for k in display_info_keys:
                    if k in info:
                        statistics[k]= info[k]

            # Ensure essential dataframes are not empty before proceeding
            if not income_statement.empty and not balance_sheet.empty and current_price is not None:
                # Extract relevant data (ensure column names match yfinance output)
                revenue = income_statement_t.get('Total Revenue')
                net_income = income_statement_t.get('Net Income')
                total_assets = balance_sheet_t.get('Total Assets')
                total_liabilities = balance_sheet_t.get('Total Liabilities')
                shareholder_equity = balance_sheet_t.get('Total Stockholder Equity')
                current_assets = balance_sheet_t.get('Total Current Assets')
                current_liabilities = balance_sheet_t.get('Total Current Liabilities')

                # Get EPS and shares outstanding from info
                eps_trailing = info.get('trailingEps')
                shares_outstanding = info.get('sharesOutstanding')


                # --- Valuation Ratios ---
                if eps_trailing and eps_trailing != 0 and current_price is not None:
                    ratios['P/E Ratio (Trailing)'] = current_price / eps_trailing
                else:
                    ratios['P/E Ratio (Trailing)'] = np.nan

                if shareholder_equity is not None and not shareholder_equity.empty and shares_outstanding and shares_outstanding != 0 and current_price is not None:
                    book_value_per_share = shareholder_equity.iloc[-1] / shares_outstanding
                    if book_value_per_share != 0:
                        ratios['P/B Ratio'] = current_price / book_value_per_share
                    else:
                        ratios['P/B Ratio'] = np.nan
                else:
                    ratios['P/B Ratio'] = np.nan

                if revenue is not None and not revenue.empty and current_price is not None and shares_outstanding and shares_outstanding != 0:
                    sales_per_share = revenue.iloc[-1] / shares_outstanding
                    if sales_per_share != 0:
                        ratios['P/S Ratio'] = current_price / sales_per_share
                    else:
                        ratios['P/S Ratio'] = np.nan
                else:
                    ratios['P/S Ratio'] = np.nan

                # --- Profitability Ratios ---
                if net_income is not None and revenue is not None and not net_income.empty and not revenue.empty and revenue.iloc[-1] != 0:
                    ratios['Net Profit Margin (%)'] = (net_income.iloc[-1] / revenue.iloc[-1]) * 100
                else:
                    ratios['Net Profit Margin (%)'] = np.nan

                if net_income is not None and shareholder_equity is not None and not net_income.empty and not shareholder_equity.empty and shareholder_equity.iloc[-1] != 0:
                    ratios['ROE (Return on Equity) (%)'] = (net_income.iloc[-1] / shareholder_equity.iloc[-1]) * 100
                else:
                    ratios['ROE (Return on Equity) (%)'] = np.nan

                if net_income is not None and total_assets is not None and not net_income.empty and not total_assets.empty and total_assets.iloc[-1] != 0:
                    ratios['ROA (Return on Assets) (%)'] = (net_income.iloc[-1] / total_assets.iloc[-1]) * 100
                else:
                    ratios['ROA (Return on Assets) (%)'] = np.nan

                # --- Liquidity Ratios ---
                if current_assets is not None and current_liabilities is not None and not current_assets.empty and not current_liabilities.empty and current_liabilities.iloc[-1] != 0:
                    ratios['Current Ratio'] = current_assets.iloc[-1] / current_liabilities.iloc[-1]
                else:
                    ratios['Current Ratio'] = np.nan

                # --- Solvency Ratios ---
                if total_liabilities is not None and shareholder_equity is not None and not total_liabilities.empty and not shareholder_equity.empty and shareholder_equity.iloc[-1] != 0:
                    ratios['Debt-to-Equity Ratio'] = total_liabilities.iloc[-1] / shareholder_equity.iloc[-1]
                else:
                    ratios['Debt-to-Equity Ratio'] = np.nan

            else:
                return {
                    "status": "error",
                    "error": "Insufficient data to calculate ratios. Please check if financial statements are available."
                }


            if income_statement_t is not None and 'Total Revenue' in income_statement_t.columns:
                revenue_series = income_statement_t['Total Revenue'].dropna()
                total_revenue = {
                    date: DataUtils.convert_to_rupees(value)
                    for date, value in revenue_series.items()
                    if pd.notnull(value)
                }
                results['Total Revenue'] = total_revenue

            if income_statement_t is not None and 'Net Income' in income_statement_t.columns:
                net_income_series = income_statement_t['Net Income'].dropna()
                net_income = {
                    date: DataUtils.convert_to_rupees(value)
                    for date, value in net_income_series.items()
                    if pd.notnull(value)
                }
                results['Net Income'] = net_income

            if shareholder_equity is not None and total_liabilities is not None and \
            not shareholder_equity.empty and not total_liabilities.empty:
                debt_to_equity_series = (total_liabilities / shareholder_equity).dropna()


        except KeyError as e:
            return {
            "status": "error",
            "error": f"Missing data for calculating ratio: {str(e)}"
        }
        except Exception as e:
            # Catch any other unexpected errors during ratio calculation
            return {
            "status": "error",
            "error": f"An unexpected error occurred during ratio calculation: {str(e)}"
        }


        # Return the collected data
        return {
            "status": "success",
            "current_price": current_price,
            "ratios": ratios,
            "statistics": statistics,
            "results": results
        }

class TechnicalAnalysis:
    """Technical analysis toolkit with improved performance and readability."""

    @staticmethod
    def add_core_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Add a core set of technical indicators."""
        try:
            # Adding trend indicators
            df["sma_20"] = ta.sma(df["close"], length=20)
            df["sma_50"] = ta.sma(df["close"], length=50)
            df["sma_200"] = ta.sma(df["close"], length=200)

            # Adding volatility indicators and volume
            daily_range = df["high"].sub(df["low"])
            adr = daily_range.rolling(window=20).mean()
            df["adrp"] = adr.div(df["close"]).mul(100)
            df["avg_20d_vol"] = df["volume"].rolling(window=20).mean()

            # Adding momentum indicators
            df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
            df["rsi"] = ta.rsi(df["close"], length=14)
            macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
            if macd is not None:
                df = pd.concat([df, macd], axis=1)

            return df

        except KeyError as e:
            raise KeyError(f"Missing column in input DataFrame: {str(e)}")
        except Exception as e:
            raise Exception(f"Error calculating indicators: {str(e)}")

    @staticmethod
    def check_trend_status(df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze the current trend status."""
        if df.empty:
            raise ValueError("DataFrame is empty. Ensure it contains valid data.")

        latest = df.iloc[-1]

 
        return {
            "above_20sma": latest["close"] > (latest["sma_20"] if latest["sma_20"] is not None else 0),
            "above_50sma": latest["close"] > (latest["sma_50"] if latest["sma_50"] is not None else 0),
            "above_200sma": latest["close"] > (latest["sma_200"] if latest["sma_200"] is not None else 0),
            "20_50_bullish": (latest["sma_20"] if latest["sma_20"] is not None else 0) > (latest["sma_50"] if latest["sma_50"] is not None else 0),
            "50_200_bullish": (latest["sma_50"] if latest["sma_50"] is not None else 0) > (latest["sma_200"] if latest["sma_200"] is not None else 0),
            "rsi": latest["rsi"] if latest["rsi"] is not None else 0,
            "macd_bullish": (latest.get("MACD_12_26_9", 0) or 0) > (latest.get("MACDs_12_26_9", 0) or 0),
        }


class RelativeStrength:
    """Tools for calculating relative strength metrics."""

    @staticmethod
    async def calculate_rs(
        market_data,
        symbol: str,
        benchmark: str = "SPY",
        lookback_periods: List[int] = [21, 63, 126, 252],
    ) -> Dict[str, float]:
        """
        Calculate relative strength compared to a benchmark across multiple timeframes.

        Args:
            market_data: Our market data fetcher instance
            symbol (str): The stock symbol to analyze
            benchmark (str): The benchmark symbol (default: SPY for S&P 500 ETF)
            lookback_periods (List[int]): Periods in trading days to calculate RS (default: [21, 63, 126, 252])

        Returns:
            Dict[str, float]: Relative strength scores for each timeframe
        """
        try:
            # Get data for both the stock and benchmark
            stock_df = await market_data.get_historical_data(
                symbol, max(lookback_periods) + 10
            )
            benchmark_df = await market_data.get_historical_data(
                benchmark, max(lookback_periods) + 10
            )

            # Calculate returns for different periods
            rs_scores = {}

            for period in lookback_periods:
                # Check if we have enough data for this period
                if len(stock_df) <= period or len(benchmark_df) <= period:
                    # Skip this period if we don't have enough data
                    continue

                # Calculate the percent change for both
                stock_return = (
                    stock_df["close"].iloc[-1] / stock_df["close"].iloc[-period] - 1
                ) * 100
                benchmark_return = (
                    benchmark_df["close"].iloc[-1] / benchmark_df["close"].iloc[-period]
                    - 1
                ) * 100

                # Calculate relative strength (stock return minus benchmark return)
                relative_performance = stock_return - benchmark_return

                # Convert to a 1-100 score (this is simplified; in practice you might use a more
                # sophisticated distribution model based on historical data)
                rs_score = min(max(50 + relative_performance, 1), 99)

                rs_scores[f"RS_{period}d"] = round(rs_score, 2)
                rs_scores[f"Return_{period}d"] = round(stock_return, 2)
                rs_scores[f"Benchmark_{period}d"] = round(benchmark_return, 2)
                rs_scores[f"Excess_{period}d"] = round(relative_performance, 2)

            return rs_scores

        except Exception as e:
            raise Exception(f"Error calculating relative strength: {str(e)}")


class VolumeProfile:
    """Tools for analyzing volume distribution by price."""

    @staticmethod
    def analyze_volume_profile(df: pd.DataFrame, num_bins: int = 10) -> Dict[str, Any]:
        """
        Create a volume profile analysis by price level.

        Args:
            df (pd.DataFrame): Historical price and volume data
            num_bins (int): Number of price bins to create (default: 10)

        Returns:
            Dict[str, Any]: Volume profile analysis
        """
        try:
            if len(df) < 20:
                raise ValueError("Not enough data for volume profile analysis")

            # Find the price range for the period
            price_min = df["low"].min()
            price_max = df["high"].max()

            # Create price bins
            bin_width = (price_max - price_min) / num_bins

            # Initialize the profile
            profile = {
                "price_min": price_min,
                "price_max": price_max,
                "bin_width": bin_width,
                "bins": [],
            }

            # Calculate volume by price bin
            for i in range(num_bins):
                bin_low = price_min + i * bin_width
                bin_high = bin_low + bin_width
                bin_mid = (bin_low + bin_high) / 2

                # Filter data in this price range
                mask = (df["low"] <= bin_high) & (df["high"] >= bin_low)
                volume_in_bin = df.loc[mask, "volume"].sum()

                # Calculate percentage of total volume
                volume_percent = (
                    (volume_in_bin / df["volume"].sum()) * 100
                    if df["volume"].sum() > 0
                    else 0
                )

                profile["bins"].append(
                    {
                        "price_low": round(bin_low, 2),
                        "price_high": round(bin_high, 2),
                        "price_mid": round(bin_mid, 2),
                        "volume": int(volume_in_bin),
                        "volume_percent": round(volume_percent, 2),
                    }
                )

            # Find the Point of Control (POC) - the price level with the highest volume
            poc_bin = max(profile["bins"], key=lambda x: x["volume"])
            profile["point_of_control"] = round(poc_bin["price_mid"], 2)

            # Find Value Area (70% of volume)
            sorted_bins = sorted(
                profile["bins"], key=lambda x: x["volume"], reverse=True
            )
            cumulative_volume = 0
            value_area_bins = []

            for bin_data in sorted_bins:
                value_area_bins.append(bin_data)
                cumulative_volume += bin_data["volume_percent"]
                if cumulative_volume >= 70:
                    break

            if value_area_bins:
                profile["value_area_low"] = round(
                    min([b["price_low"] for b in value_area_bins]), 2
                )
                profile["value_area_high"] = round(
                    max([b["price_high"] for b in value_area_bins]), 2
                )

            return profile

        except Exception as e:
            raise Exception(f"Error analyzing volume profile: {str(e)}")


class PatternRecognition:
    """Tools for detecting common chart patterns."""

    @staticmethod
    def detect_patterns(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect common chart patterns in price data.

        Args:
            df (pd.DataFrame): Historical price data

        Returns:
            Dict[str, Any]: Detected patterns and their properties
        """
        try:
            if len(df) < 60:  # Need enough data for pattern detection
                return {
                    "patterns": [],
                    "message": "Not enough data for pattern detection",
                }

            patterns = []

            # We'll use a window of the most recent data for our analysis
            recent_df = df.tail(60).copy()

            # Find local minima and maxima
            recent_df["is_min"] = (
                recent_df["low"].rolling(window=5, center=True).min()
                == recent_df["low"]
            )
            recent_df["is_max"] = (
                recent_df["high"].rolling(window=5, center=True).max()
                == recent_df["high"]
            )

            # Get the indices, prices, and dates of local minima and maxima
            minima = recent_df[recent_df["is_min"]].copy()
            maxima = recent_df[recent_df["is_max"]].copy()

            # Double Bottom Detection
            if len(minima) >= 2:
                for i in range(len(minima) - 1):
                    for j in range(i + 1, len(minima)):
                        price1 = minima.iloc[i]["low"]
                        price2 = minima.iloc[j]["low"]
                        date1 = minima.iloc[i].name
                        date2 = minima.iloc[j].name

                        # Check if the two bottoms are at similar price levels (within 3%)
                        if abs(price1 - price2) / price1 < 0.03:
                            # Check if they're at least 10 days apart
                            days_apart = (date2 - date1).days
                            if days_apart >= 10 and days_apart <= 60:
                                # Check if there's a peak in between that's at least 5% higher
                                mask = (recent_df.index > date1) & (
                                    recent_df.index < date2
                                )
                                if mask.any():
                                    max_between = recent_df.loc[mask, "high"].max()
                                    if max_between > price1 * 1.05:
                                        patterns.append(
                                            {
                                                "type": "Double Bottom",
                                                "start_date": date1.strftime(
                                                    "%Y-%m-%d"
                                                ),
                                                "end_date": date2.strftime("%Y-%m-%d"),
                                                "price_level": round(
                                                    (price1 + price2) / 2, 2
                                                ),
                                                "confidence": "Medium",
                                            }
                                        )

            # Double Top Detection (similar logic, but for maxima)
            if len(maxima) >= 2:
                for i in range(len(maxima) - 1):
                    for j in range(i + 1, len(maxima)):
                        price1 = maxima.iloc[i]["high"]
                        price2 = maxima.iloc[j]["high"]
                        date1 = maxima.iloc[i].name
                        date2 = maxima.iloc[j].name

                        if abs(price1 - price2) / price1 < 0.03:
                            days_apart = (date2 - date1).days
                            if days_apart >= 10 and days_apart <= 60:
                                mask = (recent_df.index > date1) & (
                                    recent_df.index < date2
                                )
                                if mask.any():
                                    min_between = recent_df.loc[mask, "low"].min()
                                    if min_between < price1 * 0.95:
                                        patterns.append(
                                            {
                                                "type": "Double Top",
                                                "start_date": date1.strftime(
                                                    "%Y-%m-%d"
                                                ),
                                                "end_date": date2.strftime("%Y-%m-%d"),
                                                "price_level": round(
                                                    (price1 + price2) / 2, 2
                                                ),
                                                "confidence": "Medium",
                                            }
                                        )

            # Check for potential breakouts
            close = df["close"].iloc[-1]
            recent_high = df["high"].iloc[-20:].max()
            recent_low = df["low"].iloc[-20:].min()

            # Resistance breakout
            if close > recent_high * 0.99 and close < recent_high * 1.02:
                patterns.append(
                    {
                        "type": "Resistance Breakout",
                        "price_level": round(recent_high, 2),
                        "confidence": "Medium",
                    }
                )

            # Support breakout (breakdown)
            if close < recent_low * 1.01 and close > recent_low * 0.98:
                patterns.append(
                    {
                        "type": "Support Breakdown",
                        "price_level": round(recent_low, 2),
                        "confidence": "Medium",
                    }
                )

            return {"patterns": patterns}

        except Exception as e:
            raise Exception(f"Error detecting patterns: {str(e)}")


class RiskAnalysis:
    """Tools for risk management and position sizing."""

    @staticmethod
    def calculate_position_size(
        price: float,
        stop_price: float,
        risk_amount: float,
        account_size: float,
        max_risk_percent: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Calculate appropriate position size based on risk parameters.

        Args:
            price (float): Current stock price
            stop_price (float): Stop loss price
            risk_amount (float): Amount willing to risk in dollars
            account_size (float): Total trading account size
            max_risk_percent (float): Maximum percentage of account to risk

        Returns:
            Dict[str, Any]: Position sizing recommendations
        """
        try:
            # Validate inputs
            if price <= 0 or account_size <= 0:
                raise ValueError("Price and account size must be positive")

            if price <= stop_price and stop_price != 0:
                raise ValueError(
                    "For long positions, stop price must be below entry price"
                )

            # Calculate risk per share
            risk_per_share = abs(price - stop_price)

            if risk_per_share == 0:
                raise ValueError(
                    "Risk per share cannot be zero. Entry and stop prices must differ."
                )

            # Calculate position size based on dollar risk
            shares_based_on_risk = int(risk_amount / risk_per_share)

            # Calculate maximum position size based on account risk percentage
            max_risk_dollars = account_size * (max_risk_percent / 100)
            max_shares = int(max_risk_dollars / risk_per_share)

            # Take the smaller of the two
            recommended_shares = min(shares_based_on_risk, max_shares)
            actual_dollar_risk = recommended_shares * risk_per_share

            # Calculate position cost
            position_cost = recommended_shares * price

            # Calculate R-Multiples (potential reward to risk ratios)
            r1_target = price + risk_per_share
            r2_target = price + 2 * risk_per_share
            r3_target = price + 3 * risk_per_share

            return {
                "recommended_shares": recommended_shares,
                "dollar_risk": round(actual_dollar_risk, 2),
                "risk_per_share": round(risk_per_share, 2),
                "position_cost": round(position_cost, 2),
                "account_percent_risked": round(
                    (actual_dollar_risk / account_size) * 100, 2
                ),
                "r_multiples": {
                    "r1": round(r1_target, 2),
                    "r2": round(r2_target, 2),
                    "r3": round(r3_target, 2),
                },
            }

        except Exception as e:
            raise Exception(f"Error calculating position size: {str(e)}")

    @staticmethod
    def suggest_stop_levels(df: pd.DataFrame) -> Dict[str, float]:
        """
        Suggest appropriate stop-loss levels based on technical indicators.

        Args:
            df (pd.DataFrame): Historical price data with technical indicators

        Returns:
            Dict[str, float]: Suggested stop levels
        """
        try:
            if len(df) < 20:
                raise ValueError("Not enough data for stop level analysis")

            latest = df.iloc[-1]
            close = latest["close"]

            # Calculate ATR-based stops
            atr = latest.get("atr", df["high"].iloc[-20:] - df["low"].iloc[-20:]).mean()

            # Different stop strategies
            stops = {
                "atr_1x": round(close - 1 * atr, 2),
                "atr_2x": round(close - 2 * atr, 2),
                "atr_3x": round(close - 3 * atr, 2),
                "percent_2": round(close * 0.98, 2),
                "percent_5": round(close * 0.95, 2),
                "percent_8": round(close * 0.92, 2),
            }

            # Add SMA-based stops if available
            for sma in ["sma_20", "sma_50", "sma_200"]:
                if sma in latest and not pd.isna(latest[sma]):
                    stops[sma] = round(latest[sma], 2)

            # Check for recent swing low
            recent_lows = df["low"].iloc[-20:].sort_values()
            if not recent_lows.empty:
                stops["recent_swing"] = round(recent_lows.iloc[0], 2)

            return stops

        except Exception as e:
            raise Exception(f"Error suggesting stop levels: {str(e)}")
