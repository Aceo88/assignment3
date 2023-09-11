import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import base64

app = dash.Dash(__name__)

data_url = (
    "https://raw.githubusercontent.com/Aceo88/assignment3/main/Tesla_stock_Price.csv"
)
df = pd.read_csv(data_url)

server = app.server

# Select the top 10 data points
df_price_top_10 = df.sort_values("Date").head(10)

# Define the app layout
app.layout = html.Div(
    [
        html.H1("Stock Price Data Visualization"),
        dcc.Tabs(
            id="tabs",
            value="tab-price",
            children=[
                dcc.Tab(
                    label="Stock Price",
                    value="tab-price",
                    children=[
                        dcc.Graph(id="stock-price-graph"),  # Add Stock Price graph
                        html.A(
                            html.Button("Download CSV"),
                            id="download-link",
                            download="stock_data.csv",
                            href="",
                            target="_blank",
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Volume & Chg%",
                    value="tab-volume-chg",
                    children=[
                        dcc.Dropdown(
                            id="graph-dropdown",
                            options=[
                                {"label": "Volume", "value": "volume"},
                                {"label": "Chg%", "value": "chg_percent"},
                            ],
                            value="volume",  # Initial graph choice
                            style={
                                "width": "50%"
                            },  # Adjust the dropdown width as needed
                        ),
                        dcc.Graph(id="volume-chg-graph"),
                    ],
                ),
            ],
        ),
        dcc.Download(id="download-data"),
    ]
)


# Callback to update the "stock-price-graph" when the tab is selected
@app.callback(
    Output("stock-price-graph", "figure"),
    Input("tabs", "value"),
)
def update_stock_price_graph(selected_tab):
    if selected_tab == "tab-price":
        # Create a scatter plot for Price with the top 10 data points
        fig = px.scatter(
            df_price_top_10, x="Date", y="Price", title="Stock Price (Top 10)"
        )
        return fig
    else:
        # Return a placeholder or empty figure when the tab is not "tab-price"
        return {"data": [], "layout": {}}


# Callbacks to update the Volume & Chg% graph based on the dropdown selection
@app.callback(
    Output("volume-chg-graph", "figure"),
    Input("graph-dropdown", "value"),
    prevent_initial_call=True,
)
def update_volume_chg_graph(selected_graph):
    if selected_graph == "volume":
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
    elif selected_graph == "chg_percent":
        # Sort the DataFrame by Chg% and select the top 10 data points
        df_Chg_selected = df.sort_values("Chg%", ascending=False).head(10)

        # Create a line graph for Chg%
        fig = px.line(
            df_Chg_selected,
            x="Date",
            y="Chg%",
            title="High Positive Gain",
            labels={"Date": "Date", "Chg%": "Chg%"},
            color_discrete_sequence=["green"],  # Set the line color to green
        )

        # Customize the x-axis labels for better readability
        fig.update_xaxes(tickangle=90)

        return fig


# Callback to generate and return the CSV file for download
@app.callback(
    Output("download-link", "href"),
    Input("tabs", "value"),
    prevent_initial_call=True,
)
def render_download_button(selected_tab):
    if selected_tab == "tab-price":
        href = f"data:text/csv;base64,{df_price_top_10.to_csv(index=False).encode('utf-8-sig').decode()}"
        return href

    # For other tabs, return an empty string to disable the download button
    return ""


if __name__ == "__main__":
    app.run_server(debug=True, port=8065)
