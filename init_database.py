#!/usr/bin/env python3
"""
Database initialization script for Wiki Visualizer.
This script creates all tables with the new enhanced schema.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.models.base import Base, engine, DATABASE_PATH
from app.models.entities import Continent, Country, Language, CountryLanguage

def initialize_database():
    """Initialize database with new schema"""
    try:
        print("=" * 60)
        print("🚀 Initializing Wiki Visualizer Database")
        print("=" * 60)
        
        # Check if database file exists
        if os.path.exists(DATABASE_PATH):
            print(f"📁 Database file exists at: {DATABASE_PATH}")
            print("🗑️  Removing existing database to create new schema...")
            # Remove existing database
            os.remove(DATABASE_PATH)
            print("✅ Removed existing database file")
        
        print(f"📍 Database location: {DATABASE_PATH}")
        
        # Create all tables
        print("🔨 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Verify table creation
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"✅ Successfully created {len(tables)} tables:")
        for table in sorted(tables):
            print(f"   - {table}")
        
        print("\n🎉 Database initialization completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Run the scraper to populate data: python -c 'from app.services.scraper.countries import fetch_and_store_countries; fetch_and_store_countries()'")
        print("   2. Start the application: python run.py")
        print("   3. Visit http://localhost:5000 to see your data!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = initialize_database()
    if not success:
        sys.exit(1)
