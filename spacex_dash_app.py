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

sites_names = spacex_df['Launch Site'].unique().tolist()
launch_sites = []
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})

for site in sites_names:
 launch_sites.append({'label': site, 'value': site})     

marks = range(0,11000,1000)
str_marks = [str(int) for int in marks]
 
range_marks =  {a: b for a,
            b in zip(marks, str_marks)}

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site_dropdown',
                                options=launch_sites,
                                placeholder='Select a Launch Site here',
                                 searchable = True , value = 'All Sites'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                

                                        # return the outcomes piechart for a selected site
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                
                                dcc.RangeSlider(id='payload_slider',
                                                min=0, max=10000, step=1000,
                                                marks=range_marks,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site_dropdown', component_property='value')
)
            
def get_pie_chart(site_dropdown):
    filtered_df = spacex_df.copy()
    if site_dropdown == 'All Sites':
        mask = filtered_df['class']==1
        filtered_df = filtered_df.loc[mask]
        fig = px.pie(filtered_df, 
        #values='class', 
        names='Launch Site', 
        title='Total success launches for all sites')
        return fig
    else:
        mask = filtered_df['Launch Site']==site_dropdown
        filtered_df = filtered_df.loc[mask]
        fig = px.pie(filtered_df,
        #values='class', 
        names='class', 
        title = f'Success and failed launches for site {site_dropdown}')
        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
     Output(component_id='success-payload-scatter-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value'),Input(component_id="payload_slider", component_property="value")]               
)

def update_scattergraph(site_dropdown,payload_slider):
    if site_dropdown == 'All Sites':
        low, high = payload_slider
        df  = spacex_df.copy()
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df.loc[mask], x="Payload Mass (kg)", y="class", 
            color="Booster Version",
            #size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    else:
        low, high = payload_slider
        df  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(df.loc[mask],
            x="Payload Mass (kg)", y="class", 
            color="Booster Version",
            #size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

##NOTES
# question 1. KSC
# question 2. KSC
