
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


data = pd.read_csv('MOCK_DATA.csv')


#Set the grid of the dashboard
fig = make_subplots(
    rows=4, cols=4,
    specs=[[{"rowspan": 4}, {"rowspan":2, "colspan":3}, None, None],
           [None, None, None, None],
           [None, {"rowspan":2, "type": "pie"}, {"colspan": 2, "rowspan":2}, None],
           [None, None, None, None]],
    print_grid=True)


#Bar graph on the left side
#### prep the data by grouping by families and grabbing counts.
dfg = data.groupby('family').count().reset_index()[['family','car']]
dfg = dfg.sort_values('car', ascending=True)
fig.add_trace(go.Bar(
            x=dfg.car,
            y=dfg.family,
            orientation='h'), row=1, col=1)

#Scatter plot on top
fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2], name="(1,2)"), row=1, col=2)

#Pie chart
fig.add_trace(go.Pie(values=[2, 3, 1], name="(2,1)"), row=3, col=2)

# Heatmap matrix showing day of week
data['date'] = pd.to_datetime(data['date'])
data['year'] = pd.DatetimeIndex(data['date']).year
data['month'] = pd.DatetimeIndex(data['date']).month
dfd = data.groupby(['year','month']).count().reset_index()
fig.add_trace(go.Heatmap(
                   z=dfd.car,
                   x=dfd.year,
                   y=dfd.month,
                   hoverongaps = False, showlegend=False), row=3, col=3)


#adding some overall style to all graphics and adding a title to top of page
fig.update_layout( title_text="specs examples", paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)') #height=900, width=1200,




app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig, style={'width':'95vw', 'height':'95vh', 'float':'left' }) #html styling of page
])

app.run_server(debug=True, use_reloader=True)  
#Runs the entire script and starts the server
if __name__ == '__main__':
    app.run_server(debug=True)
