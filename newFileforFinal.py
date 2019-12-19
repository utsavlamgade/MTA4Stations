import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('/Users/code/Documents/Code_Immersives/Project/Term1Final/fourStations.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
features = df.columns
Days = df['DAY'].unique()

app = dash.Dash()

app.layout = html.Div([

    html.Div([
        html.Label('DAY'),
        dcc.Dropdown(
            id='DAY',
            options=[{'label': i, 'value': i} for i in Days],
            value='',
            placeholder='Select...',
            multi=True
        )
    ],    
    style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '20px'}),    

    html.Div([
        html.Label('HOUR'),
        dcc.Slider(
            id='HOUR-slider',
            min=df['HOUR'].min(),
            max=df['HOUR'].max(),
            value=df['HOUR'].min(),
            marks={str(HOUR): str(HOUR) for HOUR in df['HOUR'].unique()},
            step=None
        ),
    ],
    style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '20px', 'margin-left': '20px'}),

    html.Div([
        dcc.Graph(id='Incoming vs Outgoing'),
    ],
    style={'width': '70%'}),
])

@app.callback(
    dash.dependencies.Output('Incoming vs Outgoing', 'figure'),
    [
        dash.dependencies.Input('HOUR-slider', 'value'),
        dash.dependencies.Input('DAY', 'value')
    ])
def update_graph(HOUR, DAY):

    filtered_df = df.loc[df["HOUR"] == HOUR]

    if (DAY != '' and DAY is not None):
        filtered_df = filtered_df[df.DAY.str.contains('|'.join(DAY))]

    traces = []
    for i in filtered_df.STATION.unique():
        df_by_STATION = filtered_df[filtered_df['STATION'] == i]
        traces.append(go.Scatter(
            x=df_by_STATION['EXIT_DIFF'],
            y=df_by_STATION['ENTRY_DIFF'],
            text=df_by_STATION['DAY'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 20,
                'line': {'width': 1.0, 'color': 'cyan'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Outgoing', 'titlefont': dict(size=18, color='darkgrey'), 'zeroline': False, 'ticks': 'outside', 'range':[-1000, 3500]},
            yaxis={'title': 'Incoming', 'titlefont': dict(size=18, color='darkgrey'), 'range': [30, 90], 'ticks': 'outside', 'range': [-2000, 4500]},
            margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)