from flask import Blueprint, render_template_string, render_template
import pandas as pd
import plotly.express as px
from app.models.base import SessionLocal
from app.models.entities import Country

visualize_bp = Blueprint('visualize', __name__)

@visualize_bp.route("/visualize")
def visualize_index():
    return render_template("visualize.html")

@visualize_bp.route("/visualize/countries")
def visualize_countries():
    db = SessionLocal()
    # Filter out countries with None values for population or area
    countries = db.query(Country).filter(
        Country.population.isnot(None),
        Country.area.isnot(None)
    ).all()
    db.close()

    if not countries:
        return "No country data available. Please run the scraper first."

    df = pd.DataFrame([{
        "Country": c.name,
        "Population": c.population,
        "Area": c.area
    } for c in countries])

    # Convert to numeric and handle any remaining None values
    df['Population'] = pd.to_numeric(df['Population'], errors='coerce')
    df['Area'] = pd.to_numeric(df['Area'], errors='coerce')
    
    # Remove any rows with NaN values
    df = df.dropna()

    if df.empty:
        return "No valid country data available after filtering."

    fig = px.scatter(df, x="Area", y="Population", text="Country",
                     size="Population", hover_name="Country",
                     title="Countries by Area & Population")
    return render_template_string(fig.to_html(full_html=False))
