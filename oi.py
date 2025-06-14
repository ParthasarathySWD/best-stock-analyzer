import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch NSE Option Chain Data
def fetch_option_chain(symbol='NIFTY'):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)  # First request to set cookies
    response = session.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch data!", response.status_code)
        return None
    
    return response.json()

# Function to extract relevant option chain data
def extract_data(data):
    records = data['records']['data']
    strike_prices = []
    ce_oi = []
    pe_oi = []
    ce_iv = []
    pe_iv = []

    for record in records:
        strike_price = record['strikePrice']
        strike_prices.append(strike_price)
        
        ce_data = record.get('CE', {})
        pe_data = record.get('PE', {})
        
        ce_oi.append(ce_data.get('openInterest', 0))
        pe_oi.append(pe_data.get('openInterest', 0))
        
        ce_iv.append(ce_data.get('impliedVolatility', 0))
        pe_iv.append(pe_data.get('impliedVolatility', 0))

    return pd.DataFrame({
        'Strike Price': strike_prices,
        'Call OI': ce_oi,
        'Put OI': pe_oi,
        'Call IV': ce_iv,
        'Put IV': pe_iv
    })

# Function to calculate PCR (Put/Call Ratio)
def calculate_pcr(df):
    total_put_oi = df['Put OI'].sum()
    total_call_oi = df['Call OI'].sum()
    pcr = total_put_oi / total_call_oi
    return pcr

# Function to calculate Max Pain
def calculate_max_pain(df):
    total_oi = df['Call OI'] + df['Put OI']
    max_pain_strike = df.loc[total_oi.idxmax(), 'Strike Price']
    return max_pain_strike

# Function to plot Option Chain Data
def plot_option_chain(df):
    plt.figure(figsize=(12, 6))
    
    # Plot Call OI
    plt.bar(df['Strike Price'], df['Call OI'], color='red', alpha=0.6, label='Call OI')
    
    # Plot Put OI
    plt.bar(df['Strike Price'], df['Put OI'], color='green', alpha=0.6, label='Put OI')
    
    plt.xlabel('Strike Price')
    plt.ylabel('Open Interest')
    plt.title('Option Chain OI Analysis')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function
def main(symbol='NIFTY'):
    # Step 1: Fetch the option chain data
    data = fetch_option_chain(symbol)
    if data is None:
        return
    
    # Step 2: Extract data into a DataFrame
    df = extract_data(data)
    
    # Step 3: Calculate PCR and Max Pain
    pcr = calculate_pcr(df)
    max_pain = calculate_max_pain(df)
    
    # Step 4: Print Results
    print(f"Put/Call Ratio (PCR): {pcr:.2f}")
    print(f"Max Pain Strike Price: {max_pain}")
    
    # Step 5: Plot the data
    plot_option_chain(df)

# Run the main function
if __name__ == "__main__":
    scrip = input("Enter the symbol for the option chain (default is 'NIFTY'): ")
    main(scrip if scrip else 'NIFTY')
