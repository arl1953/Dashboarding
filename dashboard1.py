import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Dashboard Number 1", 
                className="header-title",
                style={'textAlign': 'center', 'marginBottom': 30, 'color': 'green'}),
    ], className="header"),
    
    # Control Panel
    html.Div([
        html.Div([
            html.Label("Select Dataset:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dataset-dropdown',
                options=[
                    {'label': 'Sample Data 1', 'value': 'data1'},
                    {'label': 'Sample Data 2', 'value': 'data2'},
                    {'label': 'Sample Data 3', 'value': 'data3'}
                ],
                value='data1',
                style={'marginBottom': 15}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.Label("Date Range:", style={'fontWeight': 'bold'}),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date='2023-01-01',
                end_date='2023-12-31',
                style={'marginBottom': 15}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.Label("Chart Type:", style={'fontWeight': 'bold'}),
            dcc.RadioItems(
                id='chart-type',
                options=[
                    {'label': ' Line Chart', 'value': 'line'},
                    {'label': ' Bar Chart', 'value': 'bar'},
                    {'label': ' Scatter Plot', 'value': 'scatter'}
                ],
                value='line',
                style={'marginBottom': 15}
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'marginBottom': '20px'}),
    
    # Main content area with graphs
    html.Div([
        # First row of graphs
        html.Div([
            html.Div([
                dcc.Graph(id='main-chart')
            ], style={'width': '60%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(id='summary-chart')
            ], style={'width': '40%', 'display': 'inline-block'})
        ]),
        
        # Second row of graphs
        html.Div([
            html.Div([
                dcc.Graph(id='detail-chart-1')
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(id='detail-chart-2')
            ], style={'width': '50%', 'display': 'inline-block'})
        ])
    ]),
    
    # Footer with additional info
    html.Div([
        html.Div(id='status-info', style={'textAlign': 'center', 'color': '#7f8c8d'})
    ], style={'marginTop': '40px', 'padding': '20px', 'backgroundColor': '#ecf0f1'})
])

# Sample data generation function
def generate_sample_data(dataset_type='data1', n_points=100):
    """Generate sample data for demonstration"""
    np.random.seed(42 if dataset_type == 'data1' else 123)
    dates = pd.date_range('2023-01-01', periods=n_points, freq='D')
    
    if dataset_type == 'data1':
        values = np.cumsum(np.random.randn(n_points)) + 100
        categories = np.random.choice(['A', 'B', 'C'], n_points)
    elif dataset_type == 'data2':
        values = 50 + 20 * np.sin(np.arange(n_points) * 2 * np.pi / 30) + np.random.randn(n_points) * 5
        categories = np.random.choice(['X', 'Y', 'Z'], n_points)
    else:
        values = np.random.exponential(2, n_points) * 10
        categories = np.random.choice(['P', 'Q', 'R'], n_points)
    
    return pd.DataFrame({
        'date': dates,
        'value': values,
        'category': categories,
        'secondary_value': values * 0.8 + np.random.randn(n_points) * 3
    })

# Callbacks for interactivity
@callback(
    [Output('main-chart', 'figure'),
     Output('summary-chart', 'figure'),
     Output('detail-chart-1', 'figure'),
     Output('detail-chart-2', 'figure'),
     Output('status-info', 'children')],
    [Input('dataset-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('chart-type', 'value')]
)
def update_charts(dataset, start_date, end_date, chart_type):
    # Generate data based on selection
    df = generate_sample_data(dataset)
    
    # Filter data by date range
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Main chart
    if chart_type == 'line':
        main_fig = px.line(df_filtered, x='date', y='value', 
                          title='Main Time Series Chart')
    elif chart_type == 'bar':
        main_fig = px.bar(df_filtered.groupby('category')['value'].sum().reset_index(), 
                         x='category', y='value', 
                         title='Main Bar Chart')
    else:  # scatter
        main_fig = px.scatter(df_filtered, x='value', y='secondary_value', 
                             color='category', title='Main Scatter Plot')
    
    main_fig.update_layout(height=400)
    
    # Summary chart (pie chart of categories)
    category_counts = df_filtered['category'].value_counts()
    summary_fig = px.pie(values=category_counts.values, names=category_counts.index,
                        title='Category Distribution')
    summary_fig.update_layout(height=400)
    
    # Detail chart 1 (histogram)
    detail_fig1 = px.histogram(df_filtered, x='value', nbins=20,
                              title='Value Distribution')
    detail_fig1.update_layout(height=350)
    
    # Detail chart 2 (box plot)
    detail_fig2 = px.box(df_filtered, x='category', y='secondary_value',
                        title='Secondary Value by Category')
    detail_fig2.update_layout(height=350)
    
    # Status info
    status = f"Displaying {len(df_filtered)} data points from {start_date} to {end_date} using {dataset}"
    
    return main_fig, summary_fig, detail_fig1, detail_fig2, status

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)