from flask import Blueprint, request, render_template, current_app, jsonify, redirect, url_for
from app.services.scraper.countries import fetch_and_store_countries
from app.services.scraper.organizations import fetch_and_store_organizations
from app.services.scraper.relations import fetch_and_store_trade_relations, fetch_and_store_borders
import threading
import time
from datetime import datetime

scrape_bp = Blueprint('scrape', __name__)

# Global variable to track scraping status
scraping_status = {
    'in_progress': False,
    'completed': False,
    'current_task': '',
    'progress': 0,
    'error': None,
    'timestamp': None
}

def run_scraping_process():
    """Run the scraping process in background thread"""
    global scraping_status
    
    try:
        scraping_status['in_progress'] = True
        scraping_status['completed'] = False
        scraping_status['error'] = None
        scraping_status['progress'] = 0
        scraping_status['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Task 1: Countries
        scraping_status['current_task'] = 'Fetching countries data...'
        scraping_status['progress'] = 25
        fetch_and_store_countries()
        
        # Task 2: Organizations
        scraping_status['current_task'] = 'Processing organizations...'
        scraping_status['progress'] = 50
        fetch_and_store_organizations()
        
        # Task 3: Trade relations
        scraping_status['current_task'] = 'Analyzing trade relations...'
        scraping_status['progress'] = 75
        fetch_and_store_trade_relations()
        
        # Task 4: Borders
        scraping_status['current_task'] = 'Mapping borders...'
        scraping_status['progress'] = 90
        fetch_and_store_borders()
        
        # Completion
        scraping_status['current_task'] = 'Finalizing data...'
        scraping_status['progress'] = 100
        time.sleep(1)
        
        scraping_status['in_progress'] = False
        scraping_status['completed'] = True
        scraping_status['current_task'] = 'Scraping completed successfully!'
        
    except Exception as e:
        scraping_status['in_progress'] = False
        scraping_status['error'] = str(e)
        scraping_status['current_task'] = f'Error occurred: {str(e)}'

@scrape_bp.route("/scrape", methods=["GET", "POST"])
def scrape():
    global scraping_status
    
    if request.method == "POST":
        # Validate secret key
        secret_key = request.form.get('secret_key')
        if secret_key != 'supersecret':
            return render_template("scrape.html", error="Invalid secret key. Please try again.")
        
        if scraping_status['in_progress']:
            return render_template("scrape.html", error="Scraping already in progress. Please wait.")
        
        # Start scraping in background thread
        thread = threading.Thread(target=run_scraping_process)
        thread.daemon = True
        thread.start()
        
        return redirect(url_for('scrape.scrape_progress'))
    
    return render_template("scrape.html")

@scrape_bp.route("/scrape/progress")
def scrape_progress():
    return render_template("scrape_progress.html")

@scrape_bp.route("/scrape/status")
def scrape_status():
    global scraping_status
    return jsonify(scraping_status)

@scrape_bp.route("/scrape/completed")
def scrape_completed():
    global scraping_status
    if scraping_status['completed'] or scraping_status['error']:
        return render_template("scrape_completed.html", status=scraping_status)
    else:
        return redirect(url_for('scrape.scrape_progress'))
