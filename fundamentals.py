import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def perform_fundamental_analysis(ticker_symbol):
    """
    Performs fundamental analysis for a given ticker symbol using yfinance.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., "AAPL", "MSFT").

    Returns:
        None
    """
    print(f"--- Starting Fundamental Analysis for {ticker_symbol} ---")

    # 1. Data Collection
    print("\n1. Collecting Financial Data...")
    stock = yf.Ticker(ticker_symbol)

    try:
        # Get historical market data (e.g., last 5 years)
        hist_data = stock.history(period="5y")
        if hist_data.empty:
            print(f"Warning: No historical data found for {ticker_symbol}. Skipping historical analysis.")
            current_price = None
        else:
            current_price = hist_data['Close'].iloc[-1]
            print(f"Last closing price: ${current_price:.2f}")

        # Get income statement
        income_statement = stock.financials
        if income_statement.empty:
            print(f"Warning: No annual income statement found for {ticker_symbol}.")
        else:
            income_statement_t = income_statement.T.sort_index()
            print("\nAnnual Income Statement (last 5 rows):\n", income_statement_t.tail())

        # Get balance sheet
        balance_sheet = stock.balance_sheet
        if balance_sheet.empty:
            print(f"Warning: No annual balance sheet found for {ticker_symbol}.")
        else:
            balance_sheet_t = balance_sheet.T.sort_index()
            print("\nAnnual Balance Sheet (last 5 rows):\n", balance_sheet_t.tail())

        # Get cash flow statement
        cash_flow = stock.cashflow
        if cash_flow.empty:
            print(f"Warning: No annual cash flow statement found for {ticker_symbol}.")
        else:
            cash_flow_t = cash_flow.T.sort_index()
            print("\nAnnual Cash Flow Statement (last 5 rows):\n", cash_flow_t.tail())

        # Get key statistics and company info
        info = stock.info
        if not info:
            print(f"Warning: No general information found for {ticker_symbol}.")
        else:
            print("\nKey Company Information:")
            display_info_keys = ['marketCap', 'trailingPE', 'forwardPE', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'industry', 'sector', 'longBusinessSummary', 'sharesOutstanding', 'trailingEps']
            for k in display_info_keys:
                if k in info:
                    print(f"  {k}: {info[k]}")

    except Exception as e:
        print(f"Error during data collection for {ticker_symbol}: {e}")
        return

    # 2. Data Processing and Feature Engineering (Ratio Calculation)
    print("\n2. Calculating Key Financial Ratios...")
    ratios = {}

    try:
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
            print("Insufficient data to calculate ratios. Please check if financial statements are available.")

    except KeyError as e:
        print(f"Error: Missing data for calculating ratio. Column '{e}' not found in financial statements.")
    except Exception as e:
        print(f"An unexpected error occurred during ratio calculation: {e}")

    print("\nCalculated Key Ratios:")
    for ratio, value in ratios.items():
        if not pd.isna(value):
            print(f"  {ratio}: {value:.2f}")
        else:
            print(f"  {ratio}: N/A")

    # 3. Analysis and Interpretation (Visualizations)
    print("\n3. Generating Visualizations...")

    # Plot Revenue Trend
    if 'Total Revenue' in income_statement_t.columns and not income_statement_t['Total Revenue'].empty:
        plt.figure(figsize=(10, 6))
        income_statement_t['Total Revenue'].plot(kind='bar', color='skyblue')
        plt.title(f'{ticker_symbol} Annual Revenue Trend', fontsize=14)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Revenue (in billions)', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("  Revenue data not available for plotting.")

    # Plot Net Income Trend
    if 'Net Income' in income_statement_t.columns and not income_statement_t['Net Income'].empty:
        plt.figure(figsize=(10, 6))
        income_statement_t['Net Income'].plot(kind='bar', color='lightcoral')
        plt.title(f'{ticker_symbol} Annual Net Income Trend', fontsize=14)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Net Income (in billions)', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("  Net Income data not available for plotting.")

    # Plot Debt-to-Equity Ratio Trend (if available)
    if shareholder_equity is not None and total_liabilities is not None and \
       not shareholder_equity.empty and not total_liabilities.empty:
        debt_to_equity_series = (total_liabilities / shareholder_equity).dropna()
        if not debt_to_equity_series.empty:
            plt.figure(figsize=(10, 6))
            debt_to_equity_series.plot(kind='line', marker='o', color='green')
            plt.title(f'{ticker_symbol} Debt-to-Equity Ratio Trend', fontsize=14)
            plt.xlabel('Year', fontsize=12)
            plt.ylabel('Debt-to-Equity Ratio', fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            print("  Debt-to-Equity data not available for plotting.")
    else:
        print("  Debt-to-Equity data not available for plotting.")

    print(f"\n--- Fundamental Analysis for {ticker_symbol} Complete ---")

# --- Example Usage ---
if __name__ == "__main__":
    # You can change the ticker symbol here
    stock_ticker = "ITC.NS" # Google (Alphabet Inc.)

    perform_fundamental_analysis(stock_ticker)

    # You can analyze multiple stocks sequentially
    # print("\n\n--- Analyzing another stock (e.g., TSLA) ---")
    # perform_fundamental_analysis("TSLA")