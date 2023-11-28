from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

strDataset = "https://raw.githubusercontent.com/nelczezulueta/DATANVI-Spotify-Lecture/main/spotify-2023.csv"

dfDataset = pd.read_csv(strDataset, encoding = "ISO-8859-1")
dfDataset.head()

# Filters the dataset to get the number of songs per [released_month].
dfData1 = dfDataset["released_month"].value_counts().sort_index().rename_axis("released_month").reset_index(name = "song_count")

# Renames the [released_month] number values to their string month counterparts.
dfData1["released_month"] = dfData1["released_month"].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                              ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"])

# Displays the filtered dataset.
dfData1

# Filters the dataset to get the number of songs per [released_year] and [released_month].
dfData2 = dfDataset[["released_year", "released_month"]]
dfData2 = dfData2[dfData2["released_year"].isin(range(2019, 2024))]
dfData2["released_month"] = dfData2["released_month"].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                              ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"])

dfData2 = dfData2.groupby(["released_year", "released_month"]).size()
dfData2 = dfData2.reset_index()

dfData2.columns = ["released_year", "released_month", "song_count"]
dfData2["released_year"] = dfData2["released_year"].astype(str)

dfData2 = dfData2.pivot(index = "released_year", columns = "released_month", values = "song_count")

# Displays the filtered dataset.
dfData2

# Provided content. Do NOT alter.
cmpntTitle = html.H1(children = "SPOTIFY 2023", id = "Title")
cmpntGraphTitle1 = html.H3(children = "Song Release Bar Graph", className = "graph-title")
cmpntGraphTitle2 = html.H3(children = "Song Release Heatmap", className = "graph-title")

# Creates a [Bar Graph] for [dfData1].
graphData1 = px.bar(data_frame = dfData1,
                    x = "song_count",
                    y = "released_month",
                    orientation = "h")

# [TODO] : Change the bar colors to "#1DB954". (HINT : https://plotly.com/python/reference/bar/)
graphData1.update_traces(marker_color = '#1DB954')

# [TODO] : Change the axis titles, range, and plot background color to match the sample. The plot
#          background color is "#F8F8F8". (HINT : https://plotly.com/python/reference/layout/)
graphData1.update_layout(xaxis_title = "SONG COUNT", 
                         xaxis_range = [0, 150],
                         yaxis_title = "MONTH",
                         plot_bgcolor = '#F8F8F8')

# Place [graphData1] into a [Graph] component.
cmpntGraph1 = dcc.Graph(figure = graphData1, id = "Cmpnt-Graph-1")
# '''''''''''''''''''''''''''''''''''

heatmapColors = [(0, "#FFFFFF"), (1, "#1DB954")]

# Creates a [Heatmap] for [dfData2].
graphData2 = px.imshow(img = dfData2, color_continuous_scale = heatmapColors, aspect = "auto")

# [TODO] : Add parameters to the [px.imshow()] line ABOVE, such that it sets the Heatmap colors with the
#          provided [heatmapColors] variable, AND it sets the aspect ratio of the Heatmap to automatically
#          adjust to the provided space (i.e. to be non-square tiles).
#          (HINT : https://plotly.com/python/heatmaps/)

# [TODO] : Change the axis titles and plot background color to match the sample. The plot
#          background color is "#000000". (HINT : https://plotly.com/python/reference/layout/)
graphData2.update_layout(xaxis_title = "MONTH",
                         yaxis_title = "YEAR",
                         plot_bgcolor = '#000000')


# Place [graphData2] into a [Graph] component.
cmpntGraph2 = dcc.Graph(figure = graphData2, id = "Cmpnt-Graph-2")

application = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = application.server
server.route("/static/styles/styles.css")

# Organize the layout.
application.layout = html.Div([cmpntTitle,
                               html.Hr(),
                               dbc.Row([dbc.Col(dbc.Row([cmpntGraphTitle1, cmpntGraph1])),
                                        dbc.Col(dbc.Row([cmpntGraphTitle2, cmpntGraph2]))])])

# Run the application.
if __name__ == "__main__":
  application.run_server(port = 8051)