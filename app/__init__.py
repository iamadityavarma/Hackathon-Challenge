from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    logger.info("Starting application creation...")
    app = Flask(__name__)
    
    try:
        logger.info("Loading configuration...")
        app.config.from_object('app.config.Config')
        logger.debug(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise

    try:
        logger.info("Initializing database...")
        db.init_app(app)
        logger.info("Initializing JWT...")
        jwt.init_app(app)
    except Exception as e:
        logger.error(f"Failed to initialize extensions: {e}")
        raise

    try:
        logger.info("Registering blueprints...")
        from .routes import main_bp
        app.register_blueprint(main_bp)
        logger.info("Successfully registered blueprints")
    except Exception as e:
        logger.error(f"Failed to register blueprints: {e}")
        raise

    logger.info("Application creation completed successfully")
    return app