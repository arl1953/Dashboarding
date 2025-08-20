# Stage 1: Basic Dashboard with Single Chart
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample Data
df = pd.read_excel('dashboardexample1.xlsx')
# Assuming the DataFrame has columns 'Crowd' and 'Team'

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a simple line chart
fig = px.bar(df, x='Team', y='Crowd', title='Average Attendance')

# Define the layout
app.layout = html.Div([
    html.H1("League Attendances 23/24", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)