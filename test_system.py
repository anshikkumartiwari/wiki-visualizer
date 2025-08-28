#!/usr/bin/env python3
"""
Comprehensive test script for Wiki Visualizer functionality.
Tests database, scraping, and visualization systems.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_database_connection():
    """Test database connectivity and schema"""
    try:
        print("🔍 Testing database connection...")
        from app.models.base import SessionLocal, engine
        from app.models.entities import Country, Continent, Language
        
        db = SessionLocal()
        
        # Test basic queries
        countries_count = db.query(Country).count()
        continents_count = db.query(Continent).count()
        languages_count = db.query(Language).count()
        
        print(f"   ✅ Database connected successfully")
        print(f"   📊 Data: {countries_count} countries, {continents_count} continents, {languages_count} languages")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")
        return False

def test_scraping_system():
    """Test the scraping system"""
    try:
        print("🚀 Testing scraping system...")
        from app.services.scraper.countries import fetch_and_store_countries
        
        # This should work with our fallback system
        fetch_and_store_countries()
        print("   ✅ Scraping system works correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ Scraping test failed: {e}")
        return False

def test_visualizations():
    """Test visualization generation"""
    try:
        print("📈 Testing visualization system...")
        
        # Test individual visualization routes
        from app.routes.visualize import countries_population_area, countries_by_region, visualize_languages
        
        # Test population vs area chart
        result1 = countries_population_area()
        if '<html>' in result1 and 'Plotly' in result1:
            print("   ✅ Population vs Area chart generated successfully")
        else:
            print("   ❌ Population vs Area chart failed")
            return False
        
        # Test regional analysis
        result2 = countries_by_region()
        if '<html>' in result2 and 'Plotly' in result2:
            print("   ✅ Regional analysis chart generated successfully")
        else:
            print("   ❌ Regional analysis chart failed")
            return False
        
        # Test language visualization
        result3 = visualize_languages()
        if '<html>' in result3 and 'Plotly' in result3:
            print("   ✅ Language distribution chart generated successfully")
        else:
            print("   ❌ Language distribution chart failed")
            return False
        
        print("   🎉 All visualization tests passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Visualization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_routes():
    """Test Flask application routes"""
    try:
        print("🌐 Testing Flask routes...")
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            if response.status_code == 200:
                print("   ✅ Home page loads successfully")
            else:
                print(f"   ❌ Home page failed: {response.status_code}")
                return False
            
            # Test scrape page
            response = client.get('/scrape')
            if response.status_code == 200:
                print("   ✅ Scrape page loads successfully")
            else:
                print(f"   ❌ Scrape page failed: {response.status_code}")
                return False
            
            # Test visualization index
            response = client.get('/visualize')
            if response.status_code == 200:
                print("   ✅ Visualization index loads successfully")
            else:
                print(f"   ❌ Visualization index failed: {response.status_code}")
                return False
            
            # Test scrape status API
            response = client.get('/scrape/status')
            if response.status_code == 200:
                print("   ✅ Scrape status API works successfully")
            else:
                print(f"   ❌ Scrape status API failed: {response.status_code}")
                return False
        
        print("   🎉 All Flask route tests passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Flask route test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 WIKI VISUALIZER - COMPREHENSIVE SYSTEM TEST")
    print("=" * 70)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Scraping System", test_scraping_system),
        ("Visualization Generation", test_visualizations),
        ("Flask Routes", test_flask_routes)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name} test...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 70)
    print(f"📋 TEST SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your Wiki Visualizer is ready to use!")
        print("\n🚀 Next steps:")
        print("   1. Run: python run.py")
        print("   2. Visit: http://localhost:5000")
        print("   3. Click 'Scrape & Update' to see the new workflow")
        print("   4. Click 'Visualize' to explore your data!")
        return True
    else:
        print(f"❌ {total - passed} test(s) failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
