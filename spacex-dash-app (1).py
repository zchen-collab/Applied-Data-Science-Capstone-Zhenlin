# Import required libraries

import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe

spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()


# Create a dash application

app = dash.Dash(__name__)


# Create an app layout

app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": 40
            }
        ),

        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                *[
                    {"label": site, "value": site}
                    for site in spacex_df["Launch Site"].unique()
                ]
            ],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True
        ),

        html.Br(),

        # TASK 2: Add a pie chart to show the total successful
        # launches count for all sites.
        # If a specific launch site is selected, show
        # the Success vs. Failed counts for the site.
        html.Div(
            dcc.Graph(id="success-pie-chart")
        ),

        html.Br(),

        html.P("Payload range (Kg):"),

        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={
                0: "0",
                1000: "1000",
                2000: "2000",
                3000: "3000",
                4000: "4000",
                5000: "5000",
                6000: "6000",
                7000: "7000",
                8000: "8000",
                9000: "9000",
                10000: "10000"
            },
            value=[min_payload, max_payload]
        ),

        # TASK 4: Add a scatter chart to show the correlation
        # between payload and launch success
        html.Div(
            dcc.Graph(id="success-payload-scatter-chart")
        )
    ]
)


# TASK 2:
# Add a callback function for site-dropdown as input,
# success-pie-chart as output

@app.callback(
    Output(
        component_id="success-pie-chart",
        component_property="figure"
    ),
    Input(
        component_id="site-dropdown",
        component_property="value"
    )
)
def get_pie_chart(entered_site):

    if entered_site == "ALL":

        # Group by launch site and count successful launches
        filtered_df = (
            spacex_df
            .groupby("Launch Site")["class"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            filtered_df,
            values="class",
            names="Launch Site",
            title="Total Successful Launches by Site"
        )

        return fig

    else:

        # Filter dataframe for selected launch site
        filtered_df = spacex_df[
            spacex_df["Launch Site"] == entered_site
        ]

        # Count successful and failed launches
        outcome_counts = (
            filtered_df["class"]
            .value_counts()
            .reset_index()
        )

        outcome_counts.columns = ["class", "count"]

        # Convert class values into readable labels
        outcome_counts["Outcome"] = outcome_counts["class"].map({
            0: "Failed",
            1: "Success"
        })

        fig = px.pie(
            outcome_counts,
            values="count",
            names="Outcome",
            title=f"Launch Success for Site {entered_site}"
        )

        return fig


# TASK 4:
# Add a callback function for site-dropdown and payload-slider
# as inputs, success-payload-scatter-chart as output

@app.callback(
    Output(
        component_id="success-payload-scatter-chart",
        component_property="figure"
    ),
    [
        Input(
            component_id="site-dropdown",
            component_property="value"
        ),
        Input(
            component_id="payload-slider",
            component_property="value"
        )
    ]
)
def get_scatter_chart(entered_site, payload_range):

    # Get minimum and maximum selected payload
    low_payload = payload_range[0]
    high_payload = payload_range[1]

    # Filter dataframe based on selected payload range
    filtered_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low_payload) &
        (spacex_df["Payload Mass (kg)"] <= high_payload)
    ]

    if entered_site == "ALL":

        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for All Sites"
        )

        return fig

    else:

        # Further filter dataframe for selected launch site
        filtered_df = filtered_df[
            filtered_df["Launch Site"] == entered_site
        ]

        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Correlation between Payload and Success for Site {entered_site}"
        )

        return fig


# Run the app

if __name__ == "__main__":
    app.run()