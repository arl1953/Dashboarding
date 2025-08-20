# Stage 2: Dashboard with Interactive Dropdown
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# Create sample data

df = pd.read_excel('dashexample2.xlsx')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Average League Attendances", style={'textAlign': 'center'}),
    
    # Add dropdown for product selection
    html.Div([
        html.Label("Select Competition:"),
        dcc.Dropdown(
            id='product-dropdown',
            options=[
                {'label': 'League One', 'value': 'League One'},
                {'label': 'League Two', 'value': 'League Two'},
                {'label': 'Both Leagues', 'value': 'All'}
            ],
            value='All'  # Default value
        )
    ], style={'width': '50%', 'margin': '20px auto'}),
    
    # Graph will be updated by callback
    dcc.Graph(id='sales-chart')
])

# Callback to update chart based on dropdown selection
@callback(
    Output('sales-chart', 'figure'),
    Input('product-dropdown', 'value')  # Fixed ID
)
def update_chart(selected_product):
    if selected_product == 'All':
        # Show both products
        fig = px.line(df, x='Season', y='Crowd', color='Product', 
                     title='Avg League Attendances')
    else:
        # Filter data for selected product
        filtered_df = df[df['Product'] == selected_product]  # Fixed column name
        fig = px.line(filtered_df, x='Season', y='Crowd', 
                     title=f'Avg League Attendances - {selected_product}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)