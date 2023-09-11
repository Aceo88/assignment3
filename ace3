# Import necessary libraries
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load the dataset
data_url = "https://github.com/Aceo88/assignment3/blob/main/Tesla_stock_Price.csv"
df = pd.DataFrame(data, columns=["Date", "Price", "Open", "High", "Low", "Volume", "Chg%"])

server.app=server

# Sort the DataFrame by Date and select the top 20 data points
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date").tail(20)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Stock Price Data Visualization"),

    # Scatter plot for Price
    dcc.Graph(id='price-graph'),
    
    # Scatter plot for Volume
    dcc.Graph(id='volume-graph')
])

# Define callbacks to update the graphs
@app.callback(
    Output('price-graph', 'figure'),
    Input('price-graph', 'relayoutData')
)
def update_price_graph(relayoutData):
    # Create a scatter plot for Price
    fig = px.scatter(df, x="Date", y="Price", title="Stock Price")
    return fig

@app.callback(
    Output('volume-graph', 'figure'),
    Input('volume-graph', 'relayoutData')
)
def update_volume_graph(relayoutData):
    # Create a scatter plot for Volume
    fig = px.scatter(df, x="Date", y="Volume", title="Stock Volume")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
