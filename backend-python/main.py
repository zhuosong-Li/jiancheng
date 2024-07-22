from flask_cors import CORS

from api_utility import *
from app_config import app, db
from blueprints import register_blueprints
from mock_data_gen import *
from models import *


@app.route("/")
def hello_world():
    return "Hello World"


def main():
    """Main function to run the Flask application."""
    # Register all blueprints
    register_blueprints()
    # Run the Flask app
    app.run(
        host="0.0.0.0", port=8000, debug=True, use_reloader=False
    )  # Set debug as per your development needs


if __name__ == "__main__":
    # with app.app_context():
    # db.create_all()  # This will create the database tables under the application context.
    # shoes_rid = ["0E21922", "000000", "111111","222222"]
    # customer_name = ["Spain Customer 36", "Milan Customer 30", "Spain Customer 39", "Spain Customer 40"]
    # TestPopulateEndEntityDB(shoes_rid, customer_name)
    # TestPopulateOrdersDB(firstTime=True, reset = False)
    # with app.app_context():
        #     # reset all tables increment id
        # datagen = MockDataGenerator(db)
        # datagen.cleanAndSetup()
        # datagen.initializeEntityDataPath()
        # datagen.setupDBLocalData(terminating_layer=6)
    main()
