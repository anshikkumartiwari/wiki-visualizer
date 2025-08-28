from flask import Blueprint, render_template, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from app.models.base import SessionLocal
from app.models.entities import Country, Continent, Language, CountryLanguage
from sqlalchemy import func

visualize_bp = Blueprint('visualize', __name__)

def safe_numeric(value, default=0):
    """Safely convert to numeric value"""
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def create_chart_html(fig, title="Data Visualization"):
    """Create a full HTML page for a Plotly chart"""
    chart_html = fig.to_html(
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d']
        },
        div_id="chart"
    )
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title} - Wiki Visualizer</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" />
        <style>
            body {{ background-color: #000; color: white; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .plotly-graph-div {{ background-color: #111 !important; }}
        </style>
    </head>
    <body class="bg-black min-h-screen p-6">
        <div class="max-w-7xl mx-auto">
            <div class="mb-6 flex justify-between items-center">
                <h1 class="text-3xl font-bold text-white flex items-center gap-3">
                    <i class="fa-solid fa-chart-line text-blue-500"></i>
                    {title}
                </h1>
                <div class="flex gap-3">
                    <a href="/visualize" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors flex items-center gap-2">
                        <i class="fa-solid fa-arrow-left"></i> Back to Categories
                    </a>
                    <a href="/" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors flex items-center gap-2">
                        <i class="fa-solid fa-home"></i> Home
                    </a>
                </div>
            </div>
            <div class="bg-gray-900 rounded-xl p-6 shadow-2xl">
                {chart_html}
            </div>
        </div>
    </body>
    </html>
    """

@visualize_bp.route("/visualize")
def visualize_index():
    return render_template("visualize.html")

@visualize_bp.route("/visualize/countries")
def visualize_countries():
    return render_template("country_viz.html")

@visualize_bp.route("/visualize/countries/population-area")
def countries_population_area():
    db = SessionLocal()
    try:
        countries = db.query(Country).filter(
            Country.population.isnot(None),
            Country.area.isnot(None),
            Country.population > 0,
            Country.area > 0
        ).all()
        
        if not countries:
            return "<h1>No country data available. Please run the scraper first.</h1>"
        
        df = pd.DataFrame([{
            "Country": c.name,
            "Population": c.population,
            "Area": c.area,
            "Region": c.region or "Unknown",
            "Population_Density": c.population_density or (c.population / c.area if c.area > 0 else 0)
        } for c in countries])
        
        # Create scatter plot
        fig = px.scatter(
            df, 
            x="Area", 
            y="Population",
            hover_name="Country",
            size="Population",
            color="Region",
            log_x=True,
            log_y=True,
            title="Countries by Area vs Population (Log Scale)",
            labels={
                "Area": "Area (km²)",
                "Population": "Population"
            }
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=700,
            font=dict(color="white"),
            plot_bgcolor="#111",
            paper_bgcolor="#111"
        )
        
        return create_chart_html(fig, "Countries: Population vs Area")
        
    finally:
        db.close()

@visualize_bp.route("/visualize/countries/population-density")
def countries_population_density():
    db = SessionLocal()
    try:
        countries = db.query(Country).filter(
            Country.population.isnot(None),
            Country.area.isnot(None),
            Country.population > 0,
            Country.area > 0
        ).limit(30).all()  # Top 30 for readability
        
        if not countries:
            return "<h1>No country data available. Please run the scraper first.</h1>"
        
        # Calculate and sort by population density
        country_data = []
        for c in countries:
            density = c.population_density or (c.population / c.area if c.area > 0 else 0)
            country_data.append({
                "Country": c.name,
                "Population_Density": density,
                "Population": c.population,
                "Area": c.area
            })
        
        # Sort by density and take top 30
        country_data.sort(key=lambda x: x["Population_Density"], reverse=True)
        df = pd.DataFrame(country_data[:30])
        
        fig = px.bar(
            df,
            x="Population_Density",
            y="Country",
            orientation='h',
            title="Top 30 Countries by Population Density",
            labels={"Population_Density": "People per km²"},
            color="Population_Density",
            color_continuous_scale="Viridis"
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=800,
            font=dict(color="white"),
            plot_bgcolor="#111",
            paper_bgcolor="#111",
            yaxis={'categoryorder':'total ascending'}
        )
        
        return create_chart_html(fig, "Countries: Population Density")
        
    finally:
        db.close()

@visualize_bp.route("/visualize/countries/by-region")
def countries_by_region():
    db = SessionLocal()
    try:
        # Get region statistics
        region_stats = db.query(
            Country.region,
            func.count(Country.id).label('country_count'),
            func.sum(Country.population).label('total_population'),
            func.avg(Country.area).label('avg_area')
        ).filter(
            Country.region.isnot(None)
        ).group_by(Country.region).all()
        
        if not region_stats:
            return "<h1>No regional data available.</h1>"
        
        df = pd.DataFrame([{
            "Region": stat.region,
            "Country_Count": stat.country_count,
            "Total_Population": safe_numeric(stat.total_population, 0),
            "Avg_Area": safe_numeric(stat.avg_area, 0)
        } for stat in region_stats])
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Countries per Region",
                "Total Population by Region", 
                "Average Area by Region",
                "Population Distribution"
            ),
            specs=[
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "pie"}]
            ]
        )
        
        # Countries per region
        fig.add_trace(
            go.Bar(x=df["Region"], y=df["Country_Count"], name="Countries", marker_color="#3b82f6"),
            row=1, col=1
        )
        
        # Total population by region
        fig.add_trace(
            go.Bar(x=df["Region"], y=df["Total_Population"], name="Population", marker_color="#10b981"),
            row=1, col=2
        )
        
        # Average area by region
        fig.add_trace(
            go.Bar(x=df["Region"], y=df["Avg_Area"], name="Avg Area", marker_color="#f59e0b"),
            row=2, col=1
        )
        
        # Population pie chart
        fig.add_trace(
            go.Pie(labels=df["Region"], values=df["Total_Population"], name="Population Share"),
            row=2, col=2
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=800,
            showlegend=False,
            title_text="Regional Analysis Dashboard",
            font=dict(color="white"),
            plot_bgcolor="#111",
            paper_bgcolor="#111"
        )
        
        return create_chart_html(fig, "Countries: Regional Analysis")
        
    finally:
        db.close()

@visualize_bp.route("/visualize/countries/world-map")
def countries_world_map():
    db = SessionLocal()
    try:
        countries = db.query(Country).filter(
            Country.latitude.isnot(None),
            Country.longitude.isnot(None),
            Country.iso_code_alpha3.isnot(None)
        ).all()
        
        if not countries:
            return "<h1>No geographic data available.</h1>"
        
        df = pd.DataFrame([{
            "Country": c.name,
            "ISO": c.iso_code_alpha3,
            "Population": safe_numeric(c.population, 0),
            "Area": safe_numeric(c.area, 0),
            "Population_Density": safe_numeric(c.population_density, 0),
            "Region": c.region or "Unknown",
            "lat": c.latitude,
            "lon": c.longitude
        } for c in countries if c.iso_code_alpha3])
        
        # Create choropleth map
        fig = px.choropleth(
            df,
            locations="ISO",
            color="Population",
            hover_name="Country",
            hover_data={"Population": ":,", "Area": ":.0f", "Region": True},
            color_continuous_scale="Viridis",
            title="World Population Map"
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=600,
            font=dict(color="white"),
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular',
                bgcolor="#111"
            ),
            plot_bgcolor="#111",
            paper_bgcolor="#111"
        )
        
        return create_chart_html(fig, "World Population Map")
        
    finally:
        db.close()

@visualize_bp.route("/visualize/continents")
def visualize_continents():
    db = SessionLocal()
    try:
        continents = db.query(
            Continent.name,
            func.count(Country.id).label('country_count'),
            func.sum(Country.population).label('total_population'),
            func.sum(Country.area).label('total_area')
        ).outerjoin(Country).group_by(Continent.name).all()
        
        if not continents:
            return "<h1>No continental data available.</h1>"
        
        df = pd.DataFrame([{
            "Continent": cont.name,
            "Countries": cont.country_count or 0,
            "Population": safe_numeric(cont.total_population, 0),
            "Area": safe_numeric(cont.total_area, 0)
        } for cont in continents if cont.name])
        
        # Create treemap
        fig = px.treemap(
            df,
            path=[px.Constant("World"), "Continent"],
            values="Population",
            color="Countries",
            title="Continental Population Distribution",
            color_continuous_scale="RdYlBu"
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=600,
            font=dict(color="white"),
            plot_bgcolor="#111",
            paper_bgcolor="#111"
        )
        
        return create_chart_html(fig, "Continental Analysis")
        
    finally:
        db.close()

@visualize_bp.route("/visualize/languages")
def visualize_languages():
    db = SessionLocal()
    try:
        # Get most spoken languages
        lang_stats = db.query(
            Language.name,
            func.count(CountryLanguage.country_id).label('country_count')
        ).join(CountryLanguage).group_by(Language.name).order_by(
            func.count(CountryLanguage.country_id).desc()
        ).limit(20).all()
        
        if not lang_stats:
            return "<h1>No language data available.</h1>"
        
        df = pd.DataFrame([{
            "Language": lang.name,
            "Countries": lang.country_count
        } for lang in lang_stats])
        
        fig = px.bar(
            df,
            x="Countries",
            y="Language",
            orientation='h',
            title="Top 20 Languages by Number of Countries",
            color="Countries",
            color_continuous_scale="Blues"
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=700,
            font=dict(color="white"),
            plot_bgcolor="#111",
            paper_bgcolor="#111",
            yaxis={'categoryorder':'total ascending'}
        )
        
        return create_chart_html(fig, "Language Distribution")
        
    finally:
        db.close()

@visualize_bp.route("/visualize/organizations")
def visualize_organizations():
    # Placeholder for organizations visualization
    return "<h1>Organizations visualization coming soon!</h1>"
