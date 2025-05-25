from flask_frozen import Freezer
# Assuming your Flask app instance is named 'app' in 'src.main'
# Adjust the import path if your main script or app instance name is different
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
    freezer.freeze()
    print("Static site generated in _site directory.")

