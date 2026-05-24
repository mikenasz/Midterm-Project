
from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import pandas as pd
import sqlalchemy
import etl.extract as extract
from main import build_engine
import statsmodels
app = Dash()

engine = build_engine()

def get_dataset(engine):
    query = """
    SELECT c.country_name, p.year, p.total_population, p.population_density, p.growth_rate, h.fertility_rate, h.life_expectancy
    FROM country c
    JOIN population_metric p on c.country_id = p.country_id
    JOIN health_metric h ON p.country_id = h.country_id AND p.year = h.year
    """
    df = pd.read_sql(query, engine)
    return df

full_data = get_dataset(engine)

def get_avgs(df):
    df = df.groupby(['country_name'], as_index = False)[['population_density', 'fertility_rate', 'life_expectancy']].mean()
    df = df[df['population_density'] < 2000]
    return df

all_countries = full_data['country_name'].unique().tolist()

avg_df = get_avgs(full_data)

def make_fr_vs_le_chart():
    fig = px.scatter(
        avg_df,
        x = "life_expectancy",
        y = "fertility_rate",
        color = "country_name",
        title="Avg Fertility Rate vs Avg Life Expectancy (1990-2026)",
        trendline="ols",
        trendline_scope="overall",
        trendline_color_override="red",
        labels={
            "life_expectancy": "Average Life Expectancy",
            "fertility_rate": "Average Fertility Rate",
            "country_name": "Country"
        }
    )
    return fig

def make_fr_vs_pd_chart():
    
    fig = px.scatter(
        avg_df,
        x = "population_density",
        y = "fertility_rate",
        color = "country_name",
        trendline="ols",
        trendline_scope="overall",
        trendline_color_override="red",
        title="Avg Fertility Rate vs Avg Population Density (1990-2026)",
        labels={
            "population_density": "Average Population Density",
            "fertility_rate": "Average Fertility Rate",
            "country_name": "Country"
        }
    )
    return fig


    
def render_tab1():
    return [
        html.Div([
            html.H2("Scatter Plots"),
            html.P("These scatter plots show the relationship between fertility rate and life expectancy, and fertility rate and population density. The red line represents the overall trend across all countries."),
            dcc.Graph(figure= make_fr_vs_le_chart()),
            dcc.Graph(figure= make_fr_vs_pd_chart())
            
        ])
    ]

def render_tab2():
    return [
        html.Div([
            html.H2("Metrics over Time"),
            dcc.Dropdown(
                id="country-dropdown",
                options= all_countries,
                value= ['Germany', 'India', 'China'],
                multi = True
            ),
            dcc.Dropdown(
                id="metric-dropdown",
                options=[
                    {"label": "Fertility Rate", "value": "fertility_rate"},
                    {"label": "Growth Rate", "value": "growth_rate"},
                    {"label": "Population", "value": "total_population"},
                    {"label": "Life Expectancy", "value": "life_expectancy"},
                ],
                value="fertility_rate",
                multi = False
            ),
            dcc.Graph(id = "fr-time-chart"),
    
           
        ])
    ]
@callback(
    Output("fr-time-chart", "figure"),
    Input("country-dropdown", "value"),
    Input("metric-dropdown", "value")
)

def update_fr_time_chart(selected_countries, selected_metric):
    filtered_df = full_data[full_data['country_name'].isin(selected_countries)]
    fig = px.line(
        filtered_df,
        x = "year",
        y = selected_metric,
        color = "country_name",
        title=f"{selected_metric.replace('_', ' ').title()} vs Time (1990-2026)",
        labels={
            "year": "Year",
            selected_metric: selected_metric.replace("_", " ").title(), 
            "country_name": "Country"
        }
    )
    return fig

app.layout = html.Div([
    html.Div
    ([
        html.H1("IDB Data Project"),
        html.P("This dashboard utilizes the IDB dataset on population and health metrics across the world."),
        html.A("IDB Dataset", href = "https://www.census.gov/programs-surveys/international-programs/about/idb.html"),
    ], style={"textAlign": "center", "padding": "20px", "backgroundColor": "#94d1f5"}
    ),
    html.Div([
        html.Div([
        html.H1("Data Table Filters", style={"marginBottom": "20px", "marginTop": "6px"}),
        html.Label("Country", style={ "marginBottom": "6px", "marginTop": "6px", "display": "block"}),
        dcc.Dropdown(
            id="country-filter",
            options=[{"label": country, "value": country} for country in all_countries],
            placeholder="Select a country",
        ),
    ], style={"width": "30%", "marginBottom": "20px"}),

    html.Div([
        html.Label("Year Range", style={ "marginBottom": "20px", "marginTop": "6px", "display": "block"}),
        dcc.RangeSlider(
            id="year-filter",
            min=1990,
            max=2026,
            step=1,
            marks={year: str(year) for year in range(1990, 2027, 5)},
            value=[1990, 2026],
        ),
    ], style={"width": "60%"}),

    ], style={
        "alignItems": "center",
        "marginBottom": "24px",
    }),
    html.Br(),
    dash_table.DataTable(
            data = full_data.to_dict('records'), columns=[{"name": i, "id": i} for i in full_data.columns], page_size= 15 , sort_action= "native" , id = "data-table"
    ),
    
    dcc.Tabs(
        [
            dcc.Tab(render_tab1(), label= "Scatter"),
            dcc.Tab(render_tab2(), label= "Line")
        ]
    )
])
@callback(
    Output("data-table", "data"),
    Input("country-filter", "value"),
    Input("year-filter", "value")   
)
def filter_table(selected_country, year_range):
    filtered_df = full_data[full_data["country_name"] == selected_country] if selected_country else full_data
    
    filtered_df = filtered_df[
        (filtered_df["year"] >= year_range[0]) &
        (filtered_df["year"] <= year_range[1])
    ]
    
    return filtered_df.to_dict("records")




if __name__ == "__main__":
    app.run(debug=True)