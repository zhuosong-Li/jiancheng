from app_config import app, db
from flask_cors import CORS
from flask import Flask
from db_models.models import *

# Import any additional modules you created

def main():
    """Main function to run the Flask application."""

    # Run the Flask app
    app.run(host='0.0.0.0', port=8000, debug=True)  # Set debug as per your development needs

if __name__ == '__main__':
    main()
