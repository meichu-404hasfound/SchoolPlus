from flask import Flask, render_template
from .extensions import db, migrate
from .blueprints import register_blueprints

def create_app(config_class="app.config.DevConfig"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    @app.route("/ai_page")
    def ai_page():
        return render_template("ai_chat.html")
    return app