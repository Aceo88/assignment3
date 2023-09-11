import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import seaborn as sns

app = dash.Dash(__name__)

data_url = (
    "https://raw.githubusercontent.com/Aceo88/assignment3/main/Tesla_stock_Price.csv"
)
df = pd.read_csv(data_url)

server = app.server

# Select the top 10 data points
df_price_top_10 = df.sort_values("Date").head(10)

# Sort the DataFrame by Chg% and select the top 10 data points
df_Chg = df.sort_values("Chg%", ascending=False).head(10)

# Define the app layout
app.layout = html.Div(
    [
        html.H1("Stock Price Data Visualization"),
        dcc.Graph(id="price-graph"),  # Scatter plot for Price
        dcc.Graph(id="volume-graph"),  # Scatter plot for Volume
        dcc.Graph(id="chg-graph"),  # Line graph for Chg%
    ]
)


# Callback to update the Price graph
@app.callback(Output("price-graph", "figure"), Input("price-graph", "relayoutData"))
def update_price_graph(relayoutData):
    # Create a scatter plot for Price with the top 10 data points
    fig = px.scatter(df_price_top_10, x="Date", y="Price", title="Stock Price (Top 10)")
    return fig


# Callback to create the Highest Volume bar chart
@app.callback(Output("volume-graph", "figure"), Input("volume-graph", "relayoutData"))
def create_highest_volume_chart(relayoutData):
    # Sort the DataFrame by Volume and select the top 20 data points
    df_volume = df.sort_values("Volume", ascending=False).head(20)

    # Create a bar chart using Plotly Express
    fig = px.bar(
        df_volume,
        x="Date",
        y="Volume",
        title="Highest Volume",
        labels={"Date": "Date", "Volume": "Volume"},
        color_discrete_sequence=["red"],  # Set the bar color to red
    )

    # Customize the x-axis labels for better readability
    fig.update_xaxes(tickangle=90)

    return fig


# Callback to create the Chg% line graph
@app.callback(Output("chg-graph", "figure"), Input("chg-graph", "relayoutData"))
def create_chg_graph(relayoutData):
    # Create a line graph for Chg% with the top 10 data points
    fig = px.line(
        df_Chg,
        x="Date",
        y="Chg%",
        title="High Positive Gain",
        labels={"Date": "Date", "Chg%": "Chg%"},
        color_discrete_sequence=["green"],  # Set the line color to green
    )

    # Customize the x-axis labels for better readability
    fig.update_xaxes(tickangle=90)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8059)
