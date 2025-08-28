import requests
from app.models.base import SessionLocal
from app.models.entities import Country, Continent, Language, CountryLanguage

REST_COUNTRIES_API = "https://restcountries.com/v3.1/all"

def fetch_and_store_countries():
    db = SessionLocal()
    response = requests.get(REST_COUNTRIES_API)
    data = response.json()

    for item in data:
        try:
            # Handle name field - it could be a dict or a string
            name_data = item.get("name")
            if isinstance(name_data, dict):
                name = name_data.get("common")
            elif isinstance(name_data, str):
                name = name_data
            else:
                name = "Unknown"
            
            if not name:
                continue  # Skip countries without names
            
            capital = item.get("capital", [None])[0] if item.get("capital") else None
            population = item.get("population", 0)
            area = item.get("area", 0.0)
            iso_code = item.get("cca2")

            # continent
            continent_name = item.get("region", "Unknown")
            continent = db.query(Continent).filter_by(name=continent_name).first()
            if not continent:
                continent = Continent(name=continent_name)
                db.add(continent)
                db.commit()

            country = Country(
                name=name, capital=capital, population=population,
                area=area, iso_code=iso_code, continent_id=continent.id
            )
            db.add(country)
            db.commit()

            # languages
            langs = item.get("languages", {})
            if isinstance(langs, dict):
                for code, lang_name in langs.items():
                    lang = db.query(Language).filter_by(name=lang_name).first()
                    if not lang:
                        lang = Language(name=lang_name)
                        db.add(lang)
                        db.commit()

                    link = CountryLanguage(
                        country_id=country.id,
                        language_id=lang.id,
                        is_official=True
                    )
                    db.add(link)
                    db.commit()
                    
        except Exception as e:
            print(f"Error processing country item: {e}")
            print(f"Item data: {item}")
            continue

    db.close()
