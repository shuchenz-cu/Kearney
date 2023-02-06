### Read Input Data
import pandas as pd
df = pd.read_csv('ing_big7.csv', index_col=0)

### Build dash layout
from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
dropdown = dcc.Dropdown(df.Descrip, df.Descrip[0], multi=True, id='ing_list')

### Changing the dashboard layout
app = Dash(__name__)
app.layout = html.Div([
    html.H4("Input Values:"),
    html.Div([
        html.Div([
            daq.NumericInput(label='Total Serving',id='size', value=0),
            daq.NumericInput(label='Energy/Calories', id='cal', value=0)
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            daq.NumericInput(label='Fats', id='fats', value=0),
        daq.NumericInput(label='Saturated Fatty Acid', id='saturated', value=0)
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            daq.NumericInput(label='Carbonhydrates', id='carbon', value=0),
            daq.NumericInput(label='Sugar', id='sugar', value=0)
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            daq.NumericInput(label='Protein', id='protein', value=0),
            daq.NumericInput(label='Salt', id='salt', value=0),
        ], style={'width': '48%', 'display': 'inline-block'}),
        dropdown
    ]),
    html.Hr(),
    html.Div(id = 'big7_values'),
    html.Br(),
    html.Div(id = "ingredients")
])


### app function updates
@app.callback(
    Output('big7_valyes', 'children'),
    Input('size', 'value'),
    Input('cal', 'value'),
    Input('fats', 'value'),
    Input('saturated', 'value'),
    Input('carbon', 'value'),
    Input('sugar', 'value'),
    Input('protein', 'value'),
    Input('salt', 'value')
)
def render_values(serv, cal, fats, sat_fat, carb, sugar, protein, salt):
    return u'input big7 are {}'.format([serv, cal, fats, sat_fat, carb, sugar, protein, salt])

@app.callback(
    Output('ingredients', 'children'),
    Input('ing_list', 'value')
)
def render_ingredients_index(ing_list):
    indices = []
    for i in ing_list:
        indices.append(df.loc[df['Descrip'] == i].index.values[0])
    return u'input ingredients are {}, and names are{}'.format(indices, ing_list)

if __name__ == '__main__':
    app.run_server(debug=False,port=1234)
