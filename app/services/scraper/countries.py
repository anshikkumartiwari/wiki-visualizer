import requests
import json
from datetime import datetime
from app.models.base import SessionLocal
from app.models.entities import Country, Continent, Language, CountryLanguage
from sqlalchemy.exc import IntegrityError

REST_COUNTRIES_API = "https://restcountries.com/v3.1/all"
WORLD_BANK_API_BASE = "https://api.worldbank.org/v2/country/{}/indicator/NY.GDP.MKTP.CD,NY.GDP.PCAP.CD?format=json&date=2022&per_page=100"

def safe_get(data, *keys, default=None):
    """Safely get nested dictionary values"""
    try:
        result = data
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError, IndexError):
        return default

def safe_float(value):
    """Safely convert value to float"""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def safe_int(value):
    """Safely convert value to integer"""
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def calculate_population_density(population, area):
    """Calculate population density (people per km²)"""
    if population and area and area > 0:
        return population / area
    return None

def fetch_economic_data(iso_code):
    """Fetch GDP data from World Bank API"""
    if not iso_code:
        return None, None
    
    try:
        url = WORLD_BANK_API_BASE.format(iso_code.lower())
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and data[1]:  # World Bank API returns metadata as first element
                for item in data[1]:
                    if item.get('indicator', {}).get('id') == 'NY.GDP.MKTP.CD':
                        gdp_total = safe_float(item.get('value'))
                    elif item.get('indicator', {}).get('id') == 'NY.GDP.PCAP.CD':
                        gdp_per_capita = safe_float(item.get('value'))
                return gdp_total, gdp_per_capita
    except Exception as e:
        print(f"Error fetching economic data for {iso_code}: {e}")
    
    return None, None

def clear_existing_data(db):
    """Clear existing data to avoid duplicates"""
    try:
        # Delete in correct order to avoid foreign key constraints
        db.query(CountryLanguage).delete()
        db.query(Country).delete()
        db.query(Continent).delete()
        db.query(Language).delete()
        db.commit()
        print("Cleared existing data")
    except Exception as e:
        print(f"Error clearing data: {e}")
        db.rollback()

def fetch_and_store_countries():
    """Fetch comprehensive country data and store in database"""
    db = SessionLocal()
    
    try:
        print("Starting comprehensive country data scraping...")
        
        # Clear existing data
        clear_existing_data(db)
        
        # Try to fetch data from REST Countries API
        countries_data = None
        try:
            print("Attempting to fetch from REST Countries API...")
            response = requests.get(REST_COUNTRIES_API, timeout=30, headers={'User-Agent': 'Wiki-Visualizer/1.0'})
            if response.status_code == 200:
                countries_data = response.json()
                print(f"✅ Retrieved data for {len(countries_data)} countries from API")
            else:
                print(f"⚠️ API returned status {response.status_code}")
        except Exception as api_error:
            print(f"⚠️ API request failed: {api_error}")
        
        # Use sample data as fallback
        if not countries_data:
            print("🔄 Using sample data as fallback...")
            from .sample_data import get_sample_countries_data
            countries_data = get_sample_countries_data()
            print(f"📊 Using {len(countries_data)} sample countries for development")
        
        continent_cache = {}
        language_cache = {}
        processed_count = 0
        
        for item in countries_data:
            try:
                # Extract name information
                name_data = item.get("name", {})
                common_name = safe_get(name_data, "common")
                official_name = safe_get(name_data, "official")
                
                if not common_name:
                    continue
                
                # Basic location info
                capital_list = item.get("capital", [])
                capital = capital_list[0] if capital_list else None
                region = item.get("region")
                subregion = item.get("subregion")
                
                # ISO codes
                iso_alpha2 = item.get("cca2")
                iso_alpha3 = item.get("cca3")
                iso_numeric = item.get("ccn3")
                
                # Demographics
                population = safe_int(item.get("population"))
                area = safe_float(item.get("area"))
                population_density = calculate_population_density(population, area)
                
                # Geography
                latlng = item.get("latlng", [])
                latitude = safe_float(latlng[0]) if len(latlng) > 0 else None
                longitude = safe_float(latlng[1]) if len(latlng) > 1 else None
                landlocked = item.get("landlocked", False)
                
                # Economic indicators (Gini coefficient from REST Countries)
                gini_data = item.get("gini", {})
                gini_coefficient = None
                if gini_data:
                    # Get the most recent Gini coefficient
                    years = sorted(gini_data.keys(), reverse=True)
                    if years:
                        gini_coefficient = safe_float(gini_data[years[0]])
                
                # URLs for visual elements
                flags = item.get("flags", {})
                flag_url = flags.get("png") or flags.get("svg")
                
                coat_of_arms = item.get("coatOfArms", {})
                coat_of_arms_url = coat_of_arms.get("png") or coat_of_arms.get("svg")
                
                # JSON fields
                currencies = item.get("currencies", {})
                timezones = item.get("timezones", [])
                borders = item.get("borders", [])
                
                # Communication
                idd = item.get("idd", {})
                calling_codes = []
                if idd.get("root") and idd.get("suffixes"):
                    for suffix in idd.get("suffixes", []):
                        calling_codes.append(f"{idd['root']}{suffix}")
                
                top_level_domains = item.get("tld", [])
                
                # Handle continent
                if region:
                    if region not in continent_cache:
                        continent = db.query(Continent).filter_by(name=region).first()
                        if not continent:
                            continent = Continent(name=region)
                            db.add(continent)
                            db.flush()  # Get the ID without committing
                        continent_cache[region] = continent
                    continent = continent_cache[region]
                else:
                    continent = None
                
                # Fetch economic data from World Bank (optional, can be slow)
                gdp_total, gdp_per_capita = None, None
                if iso_alpha2 and processed_count < 50:  # Limit API calls for performance
                    gdp_total, gdp_per_capita = fetch_economic_data(iso_alpha2)
                
                # Create country record
                country = Country(
                    name=common_name,
                    official_name=official_name,
                    capital=capital,
                    region=region,
                    subregion=subregion,
                    
                    iso_code_alpha2=iso_alpha2,
                    iso_code_alpha3=iso_alpha3,
                    iso_code_numeric=iso_numeric,
                    
                    population=population,
                    area=area,
                    population_density=population_density,
                    
                    gdp_total=gdp_total,
                    gdp_per_capita=gdp_per_capita,
                    gini_coefficient=gini_coefficient,
                    
                    latitude=latitude,
                    longitude=longitude,
                    landlocked=landlocked,
                    
                    flag_url=flag_url,
                    coat_of_arms_url=coat_of_arms_url,
                    
                    currencies=currencies,
                    timezones=timezones,
                    calling_codes=calling_codes,
                    top_level_domains=top_level_domains,
                    borders=borders,
                    
                    continent_id=continent.id if continent else None
                )
                
                db.add(country)
                db.flush()  # Get the country ID
                
                # Handle languages
                languages_data = item.get("languages", {})
                if isinstance(languages_data, dict):
                    for lang_code, lang_name in languages_data.items():
                        if lang_name not in language_cache:
                            language = db.query(Language).filter_by(name=lang_name).first()
                            if not language:
                                language = Language(name=lang_name)
                                db.add(language)
                                db.flush()
                            language_cache[lang_name] = language
                        
                        language = language_cache[lang_name]
                        country_language = CountryLanguage(
                            country_id=country.id,
                            language_id=language.id,
                            is_official=True
                        )
                        db.add(country_language)
                
                processed_count += 1
                if processed_count % 20 == 0:
                    print(f"Processed {processed_count} countries...")
                    
            except Exception as e:
                print(f"Error processing country {safe_get(item, 'name', 'common', default='Unknown')}: {e}")
                continue
        
        # Commit all changes
        db.commit()
        print(f"Successfully processed {processed_count} countries")
        
    except Exception as e:
        print(f"Critical error in country scraping: {e}")
        db.rollback()
        raise e
    finally:
        db.close()
