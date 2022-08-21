import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


#load spacex data set into pandas
spacex_df = pd.read_csv("spacex_launch_dash.csv")

#get max and min payload mass
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#init Dash and app sever
app = dash.Dash(__name__)
server = app.server

uniquelaunchsites = spacex_df['Launch Site'].unique().tolist() #get unique launch sites
lsites_option = [] #this will be assigned to launch sites dropdown box options
lsites_option.append({'label': 'All Sites', 'value': 'All Sites'})
for site in uniquelaunchsites:
 lsites_option.append({'label': site, 'value': site})


#create main div
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                dcc.Dropdown(id='site_dropdown', options=lsites_option, placeholder='Select a Launch Site', 
                                             searchable = True , value = 'All Sites'),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')), #this is Pie chart
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                dcc.RangeSlider(
                                    id='payload_slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks = {
                                            0: '0 kg',
                                            1000: '1.000 kg',
                                            2000: '2.000 kg',
                                            3000: '3.000 kg',
                                            4000: '4.000 kg',
                                            5000: '5.000 kg',
                                            6000: '6.000 kg',
                                            7000: '7.000 kg',
                                            8000: '8.000 kg',
                                            9000: '9.000 kg',
                                            10000: '10.000 kg'
                                    },

                                    value=[min_payload, max_payload] #set data for range slider
                                ),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')), #this scatter chart will be rendered by callback when launch site option is selected

                                ])
#callback for main function
@app.callback(
     Output(component_id='success-pie-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value')]
)
def update_graph(site_dropdown):
    if (site_dropdown == 'All Sites'):
        df  = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df, names = 'Launch Site',hole=.3,title = 'Total Success Launches By all sites')
    else:
        df  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(df, names = 'class',hole=.3,title = 'Total Success Launches for site '+site_dropdown)
    return fig

@app.callback(
     Output(component_id='success-payload-scatter-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value'),Input(component_id="payload_slider", component_property="value")]
)
def update_scattergraph(site_dropdown,payload_slider):
    if site_dropdown == 'All Sites':
        low, high = payload_slider
        df  = spacex_df
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    else:
        low, high = payload_slider
        df  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    return fig



if __name__ == '__main__':
    app.run_server(debug=False)