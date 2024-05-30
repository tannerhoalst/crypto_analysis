import requests
import pandas as pd
from datetime import datetime, timezone

def get_historical_data(token_id, vs_currency, days):
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/market_chart?vs_currency={vs_currency}&days={days}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None

def get_coin_data(token_id):
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None

def process_historical_data(data, total_supply):
    records = []
    for i in range(len(data['prices'])):
        price = data['prices'][i][1]
        record = {
            'Timestamp': datetime.fromtimestamp(data['prices'][i][0] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            'Price (USD)': price,
            'Market Cap (USD)': data['market_caps'][i][1],
            'Fully Diluted Market Cap (USD)': price * total_supply if total_supply else 'N/A',
            '24h Volume (USD)': data['total_volumes'][i][1]
        }
        records.append(record)

    return records

def save_to_csv(records, filename):
    df = pd.DataFrame(records)
    df.to_csv(filename, mode='a', index=False, header=not pd.io.common.file_exists(filename))
    print(f"Data saved to {filename}")

def fetch_and_save_data(token_id, vs_currency, filename):
    records = []
    coin_data = get_coin_data(token_id)
    
    if coin_data:
        genesis_date = coin_data.get('genesis_date')
        if genesis_date:
            creation_date = datetime.strptime(genesis_date, '%Y-%m-%d')
            current_date = datetime.now()
            days = (current_date - creation_date).days
        else:
            days = 80
        
        total_supply = coin_data['market_data']['total_supply'] if 'market_data' in coin_data and 'total_supply' in coin_data['market_data'] else None
        data = get_historical_data(token_id, vs_currency, days)
        
        if data:
            records = process_historical_data(data, total_supply)
            if records:
                save_to_csv(records, filename)
    else:
        print("Error: Coin data not found.")

token_id = "jeo-boden"
vs_currency = "usd"
filename = "jeo_boden_market_chart_data.csv"

fetch_and_save_data(token_id, vs_currency, filename)
