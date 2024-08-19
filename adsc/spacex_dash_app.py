# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

opl = [{'label': 'All Sites', 'value': 'ALL'}]
for v in spacex_df['Launch Site'].unique().tolist():
    opl.append({'label': v, 'value': v})

marks={0: '0', 1000: '1000 kg'}
for x in range(10):
    marks[x*1000] = f"{x*1000} kg"


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', options=opl, placeholder='Select a Launch Site here', searchable = True , value = 'ALL'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks=marks,
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
     Output(component_id='success-pie-chart',component_property='figure'),
     [Input(component_id='site-dropdown',component_property='value')]
)
def get_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(filtered_df, names = 'Launch Site', title = 'Total Success Launches By All Sites')
    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(filtered_df, names = 'class', title = 'Total Success Launches for Site ' + site_dropdown)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
     Output(component_id='success-payload-scatter-chart',component_property='figure'),
     [Input(component_id='site-dropdown',component_property='value'), Input(component_id="payload-slider",component_property="value")]
)
def update_scattergraph(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        low, high = payload_slider
        df  = spacex_df
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)')
    else:
        low, high = payload_slider
        df  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
