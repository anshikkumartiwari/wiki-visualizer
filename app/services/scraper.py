import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    user_agent="WikiVisualizer/1.0 (Educational Project; anshikkumartiwari@example.com)",
    language="en"
)

def get_country_summary(name: str):
    """Fetch a short summary of a country from Wikipedia API."""
    page = wiki.page(name)
    if not page.exists():
        return None
    return {
        "title": page.title,
        "summary": page.summary[:500]  # first 500 chars
    }
