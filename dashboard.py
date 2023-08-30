import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load your data into a DataFrame
df = pd.read_csv('GeneralEsportData.csv')
df['Dates'] = [datetime(year, 1, 1) for year in df['ReleaseDate']]

# Convert the 'Dates' column to datetime
df['Dates'] = pd.to_datetime(df['Dates'])

# Calculate players_by_genre_game
players_by_genre_game = df.groupby(['Genre', 'Game'])['TotalPlayers'].sum().reset_index()

# Initialize the Dash app
app = dash.Dash(__name__)

# Link to the CSS stylesheet
external_stylesheets = ['styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Esports Earning Dashboard", style={'text-align': 'center', 'margin': '0 auto'}),
    html.Div(style={'height': '150px'}),
    html.Button("Update Charts", id="update-button"),
    
    html.Div([
        dcc.Graph(id="top-earnings-chart"),
        dcc.Graph(id="top-players-chart")
    ], style={'display': 'flex'}),
    
    dcc.Graph(id="earnings-pie-chart"),
    dcc.Graph(id="earnings-by-genre-game-bar"),
    dcc.Graph(id="total-player-growth-line"),
    
    html.Div([
        dash_table.DataTable(
            id='players-table',
            columns=[
                {'name': col, 'id': col} for col in players_by_genre_game.columns
            ],
            data=players_by_genre_game[players_by_genre_game['Genre']=='First-Person Shooter'].sort_values(by='TotalPlayers', ascending=False)[:5].to_dict('records')
        )
    ], style={'width': '30%', 'float': 'left', 'padding-left': '20px'})
])

# Define the callback to update the charts when the button is clicked
@app.callback(
    Output("top-earnings-chart", "figure"),
    Output("top-players-chart", "figure"),
    Output("earnings-pie-chart", "figure"),
    Output("earnings-by-genre-game-bar", "figure"),
    Output("total-player-growth-line", "figure"),
    Input("update-button", "n_clicks")
)
def update_charts(n_clicks):
     # Top Earnings chart
    top_earnings_df = pd.DataFrame(df.groupby('Dates')['TotalEarnings'].sum().sort_values(ascending=False)) # add [:5] for top 5
    top_earnings_chart = px.bar(top_earnings_df, x=top_earnings_df.index, y='TotalEarnings', title='Top Earnings by Date')

    # Top Players chart
    top_players_df = pd.DataFrame(df.groupby('Dates')['TotalPlayers'].sum().sort_values(ascending=False)) #add [:5] for top 5
    top_players_chart = px.bar(top_players_df, x=top_players_df.index, y='TotalPlayers', title='Top Players by Date')

    # Earnings Pie chart
    earnings_by_genre = df.groupby('Genre')['TotalEarnings'].sum().reset_index()
    earnings_pie_chart = px.pie(earnings_by_genre, values='TotalEarnings', names='Genre', title='Earnings Distribution by Genre')

    # Earnings by Genre-Game Bar chart
    earnings_by_genre_game = df.groupby(['Genre', 'Game'])['TotalEarnings'].sum().reset_index()
    earnings_by_genre_game_bar = px.bar(earnings_by_genre_game, x='Genre', y='TotalEarnings', color='Game', title='Earnings by Genre and Game')

    # Total Player Growth Line chart
    total_player_growth = df.groupby(['Dates'])['TotalPlayers'].sum().reset_index()
    total_player_growth_line = px.line(total_player_growth, x='Dates', y='TotalPlayers', title='Total Player Growth Over Time')


    return top_earnings_chart, top_players_chart, earnings_pie_chart, earnings_by_genre_game_bar, total_player_growth_line

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
