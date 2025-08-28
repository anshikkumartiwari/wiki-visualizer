from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Continent(Base):
    __tablename__ = "continent"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    population = Column(Integer)
    area = Column(Float)
    
    countries = relationship("Country", back_populates="continent")

class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    name = Column(String, nullable=False)
    official_name = Column(String)
    capital = Column(String)
    region = Column(String)  # Continent/Region
    subregion = Column(String)
    
    # Codes and Identifiers
    iso_code_alpha2 = Column(String(2))  # US, GB, etc.
    iso_code_alpha3 = Column(String(3))  # USA, GBR, etc.
    iso_code_numeric = Column(String(3)) # 840, 826, etc.
    
    # Demographics
    population = Column(Integer)
    area = Column(Float)  # in km²
    population_density = Column(Float)  # calculated field
    
    # Economics
    gdp_total = Column(Float)  # in USD
    gdp_per_capita = Column(Float)  # in USD
    gini_coefficient = Column(Float)  # inequality index
    
    # Geography
    latitude = Column(Float)
    longitude = Column(Float)
    landlocked = Column(Boolean)
    
    # Politics and Government
    government_type = Column(String)
    independence_date = Column(Date)
    
    # Culture and Society
    flag_url = Column(Text)
    coat_of_arms_url = Column(Text)
    
    # Monetary
    currencies = Column(JSON)  # Store currency info as JSON
    
    # Time and Location
    timezones = Column(JSON)  # Store multiple timezones
    
    # Additional Info
    calling_codes = Column(JSON)  # Phone calling codes
    top_level_domains = Column(JSON)  # Internet domains
    borders = Column(JSON)  # Neighboring country codes
    
    # Foreign Keys
    continent_id = Column(Integer, ForeignKey("continent.id"))
    
    # Relationships
    continent = relationship("Continent", back_populates="countries")
    languages = relationship("CountryLanguage", back_populates="country")

class Language(Base):
    __tablename__ = "language"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class CountryLanguage(Base):
    __tablename__ = "country_language"
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("country.id"))
    language_id = Column(Integer, ForeignKey("language.id"))
    is_official = Column(Boolean, default=False)
    
    # Relationships
    country = relationship("Country", back_populates="languages")
    language = relationship("Language")
