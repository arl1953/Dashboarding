# Stage 1: Basic Dashboard with Single Chart
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample Data
df = pd.read_excel('dashboardexample1.xlsx')
# If the file is not in the same directory, provide the full path
# If you have created a data folder, you can use:
# df = pd.read_excel('data/dashboardexample1.xlsx')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a simple bar chart
fig = px.bar(df, x='Team', y='Crowd', title='Average Attendance')
# For a line chart, you can use:
# fig = px.line(df, x='Team', y='Crowd', title='Average Attendance')

# Define the layout
app.layout = html.Div([
    html.H1("League Attendances 23/24", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)