from flask import Flask
import os

def create_app():
    # Get the project root directory
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(project_root, 'templates')
    
    app = Flask(__name__, template_folder=template_dir)
    app.config["SECRET_KEY"] = "supersecret"  # later move to env var

    from app.routes.main import main_bp
    from app.routes.scrape import scrape_bp
    from app.routes.visualize import visualize_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(scrape_bp)
    app.register_blueprint(visualize_bp)

    return app
