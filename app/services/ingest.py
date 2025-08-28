from app.services.scraper import get_country_summary
from app.models.base import SessionLocal
from app.models.entities import Country

def add_country(name, capital, iso_code):
    """Scrape and insert a country into DB."""
    db = SessionLocal()
    data = get_country_summary(name)
    if data:
        country = Country(name=name, capital=capital, iso_code=iso_code)
        db.add(country)
        db.commit()
    db.close()
