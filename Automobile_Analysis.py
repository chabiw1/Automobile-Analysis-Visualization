import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
# Load the data using pandas
path = '/Users/cha/Documents/lecture/untitled folder/dash/historical_automobile_sales.csv'
data = pd.read_csv(path)

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='selected_statics',
            placeholder='Select a statistic to display...'
        )
    ]),
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        value='selected_year'
    )),
    html.Div([#Add a division for output display
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),])
])

# Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True 

# Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')])

def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year',y='Automobile_Sales',title="Average Automobile Sales fluctuation over Recession Period"))

        # Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                           
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title='Average number of vehicles sold by vehicle type'))

        # Plot 3 : Pie chart for total expenditure share by vehicle type during recessions
            # grouping data for plotting
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index(name='Advertising_Expenditure')
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec,values='Advertising_Expenditure', names='Vehicle_Type', title='Total expenditure share by vehicle type during recessions'))

        # Plot 4 Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unem_rate = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unem_rate,x='unemployment_rate',y='Automobile_Sales',
                                            color='Vehicle_Type',
                                            title="Automobile Sales by Vehicle Type and Unemployment Rate",
                                            labels={'Vehicle_Type': 'Vehicle Type', 'Automobile_Sales': 'Average Sales', 'unemployment_rate': 'unemployment rate'},
                                            ))

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)])
        ]
        


    elif (selected_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == selected_year]
            
        # Plot 1 :Yearly Automobile sales using line chart for the whole period.
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas,x='Year',y='Automobile_Sales',title='Yearly Automobile sales'))

        # Plot 2 :Total Monthly Automobile sales using line chart.
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas,x='Month',y='Automobile_Sales',title='Total Month Automobile sales'))

        # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,x='Vehicle_Type',y='Automobile_Sales',title='Vehicle type sales'))

        # Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
        tad = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(tad,values='Advertising_Expenditure',names='Vehicle_Type',title='Total Advertisement Expenditure for each vehicle'))


        return [
            html.Div(className='chart-item',children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)]),
            html.Div(className='chart-item',children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)])
        ]      

if __name__ == '__main__':
    app.run_server(debug=True)