import sys
import os

# Add the parent directory (repository root) to the Python path
# This allows the script to find the 'netlify_deploy' module
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from flask_frozen import Freezer
# Assuming your Flask app instance is named 'app' in 'src.main'
# Adjust the import path if your main script or app instance name is different
# Now the import should work because the project root is in sys.path
from netlify_deploy.src.main import app

# Configure the freezer
# Set the base URL if needed, especially if using absolute URLs
# app.config["FREEZER_BASE_URL"] = "https://tools-box.netlify.app/"
app.config["FREEZER_DESTINATION"] = "_site" # Output directory
app.config["FREEZER_RELATIVE_URLS"] = True # Use relative URLs for better portability
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True # Ignore potential mimetype warnings

freezer = Freezer(app)

if __name__ == "__main__":
    print("Freezing Flask app into static site...")
    # Ensure the app context is available for URL generation
    with app.app_context():
        freezer.freeze()
    print(f"Static site generated in {app.config['FREEZER_DESTINATION']} directory.")

