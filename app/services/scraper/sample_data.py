"""
Sample data scraper for testing when REST Countries API is unavailable.
This populates the database with realistic sample data for development and testing.
"""

import json
from app.models.base import SessionLocal
from app.models.entities import Country, Continent, Language, CountryLanguage

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

def get_sample_countries_data():
    """Return comprehensive sample data for major countries"""
    return [
        {
            "name": {"common": "United States", "official": "United States of America"},
            "capital": ["Washington, D.C."],
            "region": "Americas",
            "subregion": "North America",
            "cca2": "US", "cca3": "USA", "ccn3": "840",
            "population": 331900000,
            "area": 9833517.0,
            "latlng": [38.0, -97.0],
            "landlocked": False,
            "borders": ["CAN", "MEX"],
            "currencies": {"USD": {"name": "United States dollar", "symbol": "$"}},
            "languages": {"eng": "English"},
            "timezones": ["UTC-12:00", "UTC-11:00", "UTC-10:00", "UTC-09:00", "UTC-08:00", "UTC-07:00", "UTC-06:00", "UTC-05:00", "UTC-04:00", "UTC+10:00", "UTC+12:00"],
            "flags": {"png": "https://flagcdn.com/w320/us.png", "svg": "https://flagcdn.com/us.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/us.png"},
            "idd": {"root": "+1", "suffixes": [""]},
            "tld": [".us"],
            "gini": {"2018": 41.4}
        },
        {
            "name": {"common": "China", "official": "People's Republic of China"},
            "capital": ["Beijing"],
            "region": "Asia",
            "subregion": "Eastern Asia",
            "cca2": "CN", "cca3": "CHN", "ccn3": "156",
            "population": 1439323776,
            "area": 9596961.0,
            "latlng": [35.0, 105.0],
            "landlocked": False,
            "borders": ["AFG", "BTN", "MMR", "HKG", "IND", "KAZ", "KGZ", "LAO", "MAC", "MNG", "PAK", "RUS", "TJK", "VNM"],
            "currencies": {"CNY": {"name": "Chinese yuan", "symbol": "¥"}},
            "languages": {"zho": "Chinese"},
            "timezones": ["UTC+08:00"],
            "flags": {"png": "https://flagcdn.com/w320/cn.png", "svg": "https://flagcdn.com/cn.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/cn.png"},
            "idd": {"root": "+8", "suffixes": ["6"]},
            "tld": [".cn", ".中国", ".中國"],
            "gini": {"2016": 38.5}
        },
        {
            "name": {"common": "India", "official": "Republic of India"},
            "capital": ["New Delhi"],
            "region": "Asia",
            "subregion": "Southern Asia",
            "cca2": "IN", "cca3": "IND", "ccn3": "356",
            "population": 1380004385,
            "area": 3287263.0,
            "latlng": [20.0, 77.0],
            "landlocked": False,
            "borders": ["AFG", "BGD", "BTN", "MMR", "CHN", "NPL", "PAK"],
            "currencies": {"INR": {"name": "Indian rupee", "symbol": "₹"}},
            "languages": {"hin": "Hindi", "eng": "English"},
            "timezones": ["UTC+05:30"],
            "flags": {"png": "https://flagcdn.com/w320/in.png", "svg": "https://flagcdn.com/in.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/in.png"},
            "idd": {"root": "+9", "suffixes": ["1"]},
            "tld": [".in"],
            "gini": {"2011": 35.7}
        },
        {
            "name": {"common": "Brazil", "official": "Federative Republic of Brazil"},
            "capital": ["Brasília"],
            "region": "Americas",
            "subregion": "South America",
            "cca2": "BR", "cca3": "BRA", "ccn3": "076",
            "population": 212559417,
            "area": 8515767.0,
            "latlng": [-10.0, -55.0],
            "landlocked": False,
            "borders": ["ARG", "BOL", "COL", "GUF", "GUY", "PRY", "PER", "SUR", "URY", "VEN"],
            "currencies": {"BRL": {"name": "Brazilian real", "symbol": "R$"}},
            "languages": {"por": "Portuguese"},
            "timezones": ["UTC-05:00", "UTC-04:00", "UTC-03:00", "UTC-02:00"],
            "flags": {"png": "https://flagcdn.com/w320/br.png", "svg": "https://flagcdn.com/br.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/br.png"},
            "idd": {"root": "+5", "suffixes": ["5"]},
            "tld": [".br"],
            "gini": {"2019": 53.4}
        },
        {
            "name": {"common": "Russia", "official": "Russian Federation"},
            "capital": ["Moscow"],
            "region": "Europe",
            "subregion": "Eastern Europe",
            "cca2": "RU", "cca3": "RUS", "ccn3": "643",
            "population": 144104080,
            "area": 17098242.0,
            "latlng": [60.0, 100.0],
            "landlocked": False,
            "borders": ["AZE", "BLR", "CHN", "EST", "FIN", "GEO", "KAZ", "PRK", "LVA", "LTU", "MNG", "NOR", "POL", "UKR"],
            "currencies": {"RUB": {"name": "Russian ruble", "symbol": "₽"}},
            "languages": {"rus": "Russian"},
            "timezones": ["UTC+03:00", "UTC+04:00", "UTC+05:00", "UTC+06:00", "UTC+07:00", "UTC+08:00", "UTC+09:00", "UTC+10:00", "UTC+11:00", "UTC+12:00"],
            "flags": {"png": "https://flagcdn.com/w320/ru.png", "svg": "https://flagcdn.com/ru.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/ru.png"},
            "idd": {"root": "+7", "suffixes": [""]},
            "tld": [".ru", ".рф"],
            "gini": {"2018": 37.5}
        },
        {
            "name": {"common": "Germany", "official": "Federal Republic of Germany"},
            "capital": ["Berlin"],
            "region": "Europe",
            "subregion": "Western Europe",
            "cca2": "DE", "cca3": "DEU", "ccn3": "276",
            "population": 83240525,
            "area": 357114.0,
            "latlng": [51.0, 9.0],
            "landlocked": False,
            "borders": ["AUT", "BEL", "CZE", "DNK", "FRA", "LUX", "NLD", "POL", "CHE"],
            "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
            "languages": {"deu": "German"},
            "timezones": ["UTC+01:00"],
            "flags": {"png": "https://flagcdn.com/w320/de.png", "svg": "https://flagcdn.com/de.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/de.png"},
            "idd": {"root": "+4", "suffixes": ["9"]},
            "tld": [".de"],
            "gini": {"2016": 31.9}
        },
        {
            "name": {"common": "Japan", "official": "Japan"},
            "capital": ["Tokyo"],
            "region": "Asia",
            "subregion": "Eastern Asia",
            "cca2": "JP", "cca3": "JPN", "ccn3": "392",
            "population": 125836021,
            "area": 377930.0,
            "latlng": [36.0, 138.0],
            "landlocked": False,
            "borders": [],
            "currencies": {"JPY": {"name": "Japanese yen", "symbol": "¥"}},
            "languages": {"jpn": "Japanese"},
            "timezones": ["UTC+09:00"],
            "flags": {"png": "https://flagcdn.com/w320/jp.png", "svg": "https://flagcdn.com/jp.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/jp.png"},
            "idd": {"root": "+8", "suffixes": ["1"]},
            "tld": [".jp", ".日本"],
            "gini": {"2013": 32.9}
        },
        {
            "name": {"common": "France", "official": "French Republic"},
            "capital": ["Paris"],
            "region": "Europe",
            "subregion": "Western Europe",
            "cca2": "FR", "cca3": "FRA", "ccn3": "250",
            "population": 67391582,
            "area": 551695.0,
            "latlng": [46.0, 2.0],
            "landlocked": False,
            "borders": ["AND", "BEL", "DEU", "ITA", "LUX", "MCO", "ESP", "CHE"],
            "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
            "languages": {"fra": "French"},
            "timezones": ["UTC-10:00", "UTC-09:30", "UTC-09:00", "UTC-08:00", "UTC-04:00", "UTC-03:00", "UTC+01:00", "UTC+03:00", "UTC+04:00", "UTC+05:00", "UTC+11:00", "UTC+12:00"],
            "flags": {"png": "https://flagcdn.com/w320/fr.png", "svg": "https://flagcdn.com/fr.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/fr.png"},
            "idd": {"root": "+3", "suffixes": ["3"]},
            "tld": [".fr"],
            "gini": {"2018": 32.4}
        },
        {
            "name": {"common": "United Kingdom", "official": "United Kingdom of Great Britain and Northern Ireland"},
            "capital": ["London"],
            "region": "Europe",
            "subregion": "Northern Europe",
            "cca2": "GB", "cca3": "GBR", "ccn3": "826",
            "population": 67886011,
            "area": 242495.0,
            "latlng": [54.0, -2.0],
            "landlocked": False,
            "borders": ["IRL"],
            "currencies": {"GBP": {"name": "British pound", "symbol": "£"}},
            "languages": {"eng": "English"},
            "timezones": ["UTC-08:00", "UTC-05:00", "UTC-04:00", "UTC-03:00", "UTC-02:00", "UTC+00:00", "UTC+01:00", "UTC+06:00"],
            "flags": {"png": "https://flagcdn.com/w320/gb.png", "svg": "https://flagcdn.com/gb.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/gb.png"},
            "idd": {"root": "+4", "suffixes": ["4"]},
            "tld": [".uk"],
            "gini": {"2017": 35.1}
        },
        {
            "name": {"common": "Australia", "official": "Commonwealth of Australia"},
            "capital": ["Canberra"],
            "region": "Oceania",
            "subregion": "Australia and New Zealand",
            "cca2": "AU", "cca3": "AUS", "ccn3": "036",
            "population": 25687041,
            "area": 7692024.0,
            "latlng": [-27.0, 133.0],
            "landlocked": False,
            "borders": [],
            "currencies": {"AUD": {"name": "Australian dollar", "symbol": "$"}},
            "languages": {"eng": "English"},
            "timezones": ["UTC+05:00", "UTC+06:30", "UTC+07:00", "UTC+08:00", "UTC+08:45", "UTC+09:30", "UTC+10:00", "UTC+10:30", "UTC+11:00"],
            "flags": {"png": "https://flagcdn.com/w320/au.png", "svg": "https://flagcdn.com/au.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/au.png"},
            "idd": {"root": "+6", "suffixes": ["1"]},
            "tld": [".au"],
            "gini": {"2018": 34.4}
        },
        {
            "name": {"common": "Canada", "official": "Canada"},
            "capital": ["Ottawa"],
            "region": "Americas",
            "subregion": "North America",
            "cca2": "CA", "cca3": "CAN", "ccn3": "124",
            "population": 38005238,
            "area": 9984670.0,
            "latlng": [60.0, -95.0],
            "landlocked": False,
            "borders": ["USA"],
            "currencies": {"CAD": {"name": "Canadian dollar", "symbol": "$"}},
            "languages": {"eng": "English", "fra": "French"},
            "timezones": ["UTC-08:00", "UTC-07:00", "UTC-06:00", "UTC-05:00", "UTC-04:00", "UTC-03:30"],
            "flags": {"png": "https://flagcdn.com/w320/ca.png", "svg": "https://flagcdn.com/ca.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/ca.png"},
            "idd": {"root": "+1", "suffixes": [""]},
            "tld": [".ca"],
            "gini": {"2017": 33.3}
        },
        # Adding smaller countries for diversity
        {
            "name": {"common": "Monaco", "official": "Principality of Monaco"},
            "capital": ["Monaco"],
            "region": "Europe",
            "subregion": "Western Europe",
            "cca2": "MC", "cca3": "MCO", "ccn3": "492",
            "population": 39244,
            "area": 2.02,
            "latlng": [43.73, 7.42],
            "landlocked": False,
            "borders": ["FRA"],
            "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
            "languages": {"fra": "French"},
            "timezones": ["UTC+01:00"],
            "flags": {"png": "https://flagcdn.com/w320/mc.png", "svg": "https://flagcdn.com/mc.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/mc.png"},
            "idd": {"root": "+3", "suffixes": ["77"]},
            "tld": [".mc"],
            "gini": {}
        },
        {
            "name": {"common": "Singapore", "official": "Republic of Singapore"},
            "capital": ["Singapore"],
            "region": "Asia",
            "subregion": "South-Eastern Asia",
            "cca2": "SG", "cca3": "SGP", "ccn3": "702",
            "population": 5850342,
            "area": 710.0,
            "latlng": [1.37, 103.8],
            "landlocked": False,
            "borders": [],
            "currencies": {"SGD": {"name": "Singapore dollar", "symbol": "$"}},
            "languages": {"zho": "Chinese", "eng": "English", "msa": "Malay", "tam": "Tamil"},
            "timezones": ["UTC+08:00"],
            "flags": {"png": "https://flagcdn.com/w320/sg.png", "svg": "https://flagcdn.com/sg.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/sg.png"},
            "idd": {"root": "+6", "suffixes": ["5"]},
            "tld": [".sg", ".新加坡", ".சிங்கப்பூர்"],
            "gini": {}
        },
        {
            "name": {"common": "Mongolia", "official": "Mongolia"},
            "capital": ["Ulaanbaatar"],
            "region": "Asia",
            "subregion": "Eastern Asia",
            "cca2": "MN", "cca3": "MNG", "ccn3": "496",
            "population": 3278292,
            "area": 1564110.0,
            "latlng": [46.0, 105.0],
            "landlocked": True,
            "borders": ["CHN", "RUS"],
            "currencies": {"MNT": {"name": "Mongolian tögrög", "symbol": "₮"}},
            "languages": {"mon": "Mongolian"},
            "timezones": ["UTC+07:00", "UTC+08:00"],
            "flags": {"png": "https://flagcdn.com/w320/mn.png", "svg": "https://flagcdn.com/mn.svg"},
            "coatOfArms": {"png": "https://mainfacts.com/media/images/coats_of_arms/mn.png"},
            "idd": {"root": "+9", "suffixes": ["76"]},
            "tld": [".mn"],
            "gini": {"2018": 32.7}
        }
    ]

def populate_with_sample_data():
    """Populate database with comprehensive sample data"""
    db = SessionLocal()
    
    try:
        print("🚀 Starting sample data population...")
        
        # Clear existing data
        clear_existing_data(db)
        
        sample_data = get_sample_countries_data()
        
        continent_cache = {}
        language_cache = {}
        processed_count = 0
        
        for item in sample_data:
            try:
                # Extract name information
                name_data = item.get("name", {})
                common_name = name_data.get("common")
                official_name = name_data.get("official")
                
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
                population = item.get("population")
                area = item.get("area")
                population_density = population / area if population and area and area > 0 else None
                
                # Geography
                latlng = item.get("latlng", [])
                latitude = latlng[0] if len(latlng) > 0 else None
                longitude = latlng[1] if len(latlng) > 1 else None
                landlocked = item.get("landlocked", False)
                
                # Economic indicators
                gini_data = item.get("gini", {})
                gini_coefficient = None
                if gini_data:
                    years = sorted(gini_data.keys(), reverse=True)
                    if years:
                        gini_coefficient = float(gini_data[years[0]])
                
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
                            db.flush()
                        continent_cache[region] = continent
                    continent = continent_cache[region]
                else:
                    continent = None
                
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
                db.flush()
                
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
                print(f"✅ Processed: {common_name}")
                
            except Exception as e:
                print(f"❌ Error processing country {item.get('name', {}).get('common', 'Unknown')}: {e}")
                continue
        
        # Commit all changes
        db.commit()
        print(f"🎉 Successfully populated database with {processed_count} countries!")
        
        # Print summary
        print("\n📊 Data Summary:")
        total_countries = db.query(Country).count()
        total_continents = db.query(Continent).count()
        total_languages = db.query(Language).count()
        print(f"   - Countries: {total_countries}")
        print(f"   - Continents: {total_continents}")
        print(f"   - Languages: {total_languages}")
        
        return True
        
    except Exception as e:
        print(f"❌ Critical error in sample data population: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()

if __name__ == "__main__":
    success = populate_with_sample_data()
    if success:
        print("\n✨ Sample data population completed!")
        print("You can now:")
        print("  1. Start the application: python run.py")
        print("  2. Visit http://localhost:5000 to see the visualizations!")
    else:
        print("❌ Sample data population failed!")
