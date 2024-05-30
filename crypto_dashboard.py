# stock_percentage_change_dashboard.py

import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go

# Load the data
stock1 = pd.read_csv('jeo_boden_market_chart_data.csv')

# Convert Timestamp column to datetime
stock1['Timestamp'] = pd.to_datetime(stock1['Timestamp'])

# Calculate percentage change from the first data point
first_price = stock1['Price (USD)'].iloc[0]
stock1['Pct_Change'] = ((stock1['Price (USD)'] - first_price) / first_price) * 100

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock 1 Percentage Change from First Data Point"),
    dcc.Graph(
        id='stock1-comparison-graph',
        figure={
            'data': [
                go.Scatter(
                    x=stock1['Timestamp'],
                    y=stock1['Pct_Change'],
                    mode='lines',
                    name='Stock 1',
                    line=dict(shape='linear', dash='solid')  # Ensure no trend lines are added
                )
            ],
            'layout': go.Layout(
                title='Percentage Change of Stock 1 from First Data Point',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Percentage Change'},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
