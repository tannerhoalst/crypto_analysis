import requests
import pandas as pd

def fetch_trading_data(token_address, api_key):
    url = f'https://solana-mainnet.g.alchemy.com/v2/{api_key}'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getProgramAccounts",
        "params": [
            token_address,
            {
                "encoding": "jsonParsed"
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error: Unable to parse JSON response.")
            return None
    else:
        print(f"Error: Received response with status code {response.status_code}")
        print(f"Response body: {response.text}")
        return None

def process_trading_data(data):
    if not data or 'result' not in data:
        print("Error: Invalid data format received from API.")
        return []

    trader_profits = {}
    
    for account in data['result']:
        account_info = account.get('account', {}).get('data', {}).get('parsed', {}).get('info', {})
        trader_address = account_info.get('owner')
        profit = account_info.get('tokenAmount', {}).get('amount', 0)
        
        if trader_address in trader_profits:
            trader_profits[trader_address] += int(profit)
        else:
            trader_profits[trader_address] = int(profit)
    
    top_traders = sorted(trader_profits.items(), key=lambda x: x[1], reverse=True)[:100]
    return top_traders

def save_to_csv(traders, filename):
    df = pd.DataFrame(traders, columns=['Address', 'Profit'])
    df.to_csv(filename, index=False)

def main():
    token_address = input("Enter the Solana token contract address: ")
    api_key = input("Enter your Alchemy API key: ")
    
    trading_data = fetch_trading_data(token_address, api_key)
    
    if trading_data is None:
        print("Failed to fetch trading data. Exiting.")
        return
    
    top_traders = process_trading_data(trading_data)
    
    if not top_traders:
        print("No valid trading data found. Exiting.")
        return
    
    output_filename = f'{token_address}_top_traders.csv'
    save_to_csv(top_traders, output_filename)
    print(f'Top traders saved to {output_filename}')

if __name__ == '__main__':
    main()

    
