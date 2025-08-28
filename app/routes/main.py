from flask import Blueprint, render_template_string

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return "<h1>Wiki Visualizer - Home</h1><p>Visit /chart for demo.</p>"


@main_bp.route("/chart")
def chart():
    try:
        import plotly.express as px
        import pandas as pd
    except Exception as exc:
        return render_template_string(f"<pre>Plotly/Pandas not available: {exc}</pre>")

    df = pd.DataFrame({
        "Country": ["India", "USA", "China"],
        "Population": [1400, 330, 1440],
    })
    fig = px.bar(df, x="Country", y="Population", title="Population Chart")
    # Return raw HTML to avoid Jinja parsing errors on Plotly's HTML
    return fig.to_html(full_html=True, include_plotlyjs="cdn")
