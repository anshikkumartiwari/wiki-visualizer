from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Continent(Base):
    __tablename__ = "continent"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    population = Column(Integer)
    area = Column(Float)

    countries = relationship("Country", back_populates="continent")

class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    capital = Column(String)
    population = Column(Integer)
    area = Column(Float)
    iso_code = Column(String)
    continent_id = Column(Integer, ForeignKey("continent.id"))

    continent = relationship("Continent", back_populates="countries")

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
