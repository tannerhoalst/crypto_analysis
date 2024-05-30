import requests
import pandas as pd
from datetime import datetime
import time

def get_historical_data(address, adress_type, candle_time, start_time, end_time):
    url = "https://public-api.birdeye.so/defi/history_price?address={address}&address_type={adress_type}&type={candle_time}&time_from={start_time}&time_to={end_time}"
    headers = {"X-API-KEY": "[REMOVED]"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None

def process_historical_data(data):
    if 'data' not in data:
        print("No data found.")
        return None

    records = []
    for entry in data['data']:
        record = {
            'Timestamp': datetime.utcfromtimestamp(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
            'Price (USD)': entry.get('price', 'N/A'),
            'Liquidity (USD)': entry.get('liquidity', {}).get('usd', 'N/A'),
            '24h Volume (USD)': entry.get('volume', {}).get('24h', 'N/A')
        }
        records.append(record)

    return records

def save_to_csv(records, filename):
    df = pd.DataFrame(records)
    df.to_csv(filename, mode='a', index=False, header=not pd.io.common.file_exists(filename))
    print(f"Data saved to {filename}")

def fetch_and_save_data(pair_address, start_time, end_time, filename):
    records = []
    current_time = start_time

    while current_time < end_time:
        batch_end_time = min(current_time + 60 * 60, end_time)  # Fetch data in hourly intervals
        data = get_historical_data(pair_address, current_time, batch_end_time)
        if data:
            batch_records = process_historical_data(data)
            if batch_records:
                records.extend(batch_records)
        
        current_time = batch_end_time
        
        if len(records) >= 800:
            save_to_csv(records, filename)
            records = []
            time.sleep(60) 

    if records:
        save_to_csv(records, filename)

sol_usdc_pair_address = "SOL_USDC_PAIR_ADDRESS"
start_time = int(datetime(2023, 1, 1).timestamp())
end_time = int(datetime(2023, 1, 2).timestamp())
filename = "sol_usdc_historical_data.csv"

fetch_and_save_data(sol_usdc_pair_address, start_time, end_time, filename)
