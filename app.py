# ===========================================================
#  COPYRIGHT © 2024 Sueun Cho. ALL RIGHTS RESERVED.
#
#  This code is the intellectual property of Sueun Cho. 
#  Unauthorized reproduction, distribution, or use of this code 
#  is strictly prohibited. This notice must not be removed.
#  For permission to use this code or any part thereof, please 
#  contact the copyright holder.
#  
#  저작권 © 2024 조수은. "코드" 작성에 대해서만 모든 권리 보유.
#
#  이 코드는 조수은의 지적 재산입니다. 이 코드의 무단 복제, 배포, 
#  또는 사용은 엄격히 금지됩니다. 이 주석을 삭제하지 마십시오.
#  이 코드 또는 그 일부를 사용하려면 저작권자에게 문의하십시오.
#  E-mail : sueun.dev@gamil.com
#  gitrhub : sueun-dev
# ===========================================================

from flask import (
    Flask, request, render_template, send_from_directory, abort, 
    Response, redirect, url_for, flash, 
)  # Import necessary Flask modules and functions

from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database management
from flask_migrate import Migrate  # Import Migrate for database migrations
from functools import wraps  # Import wraps for decorating functions
import os  # Import os for environment variable handling
import time  # Import time for time-related functions
from dotenv import load_dotenv  # Import load_dotenv for loading environment variables
from werkzeug.security import generate_password_hash, check_password_hash  # Import security functions


load_dotenv()  # Load environment variables from a .env file

app = Flask(__name__)  # Initialize the Flask application
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Set the Flask secret key


# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")  # Set the database URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable SQLAlchemy modification tracking
app.config["SQLALCHEMY_ECHO"] = False  # Disable SQL command echoing


db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app for database management
migrate = Migrate(app, db)  # Set up Flask-Migrate for database migrations

UPLOAD_FOLDER = "uploads"  # Define the directory for file uploads
ALLOWED_EXTENSIONS = {"pdf"}  # Set allowed file extensions for upload
MAX_CONTENT_LENGTH = 12 * 1024 * 1024  # 12 MB, Define maximum file upload size
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  # Configure Flask to use the defined upload folder
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH  # Set the maximum upload size limit in Flask

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the upload directory if it doesn't exist

# Authentication settings
USERNAME = os.getenv("UPLOAD_USERNAME")  # Retrieve the upload username from environment variables
PASSWORD = generate_password_hash(os.getenv("UPLOAD_PASSWORD"), method="pbkdf2:sha256")  
# Retrieve and hash the upload password using PBKDF2 with SHA-256 for secure storage

MAX_ATTEMPTS = 7  # Set the maximum number of allowed login attempts
BLOCK_TIME = 24 * 60 * 60  # 24 hours in seconds, Set the block time after max login attempts are exceeded

# Track login attempts
# 누가 나에게 3가지 소원을 나에게 묻는다면, 첫째도 정보공유, 둘째도 정보공유, 셋째도 정보공유라고 대답할 것이다.
login_attempts = {}  # Initialize a dictionary to track login attempts by IP address

def check_auth(username, password):
    """Check if the provided username and password are correct."""
    return username == USERNAME and check_password_hash(PASSWORD, password)  
    # Compares the provided username and hashed password with the stored values

from flask import Response

def authenticate():
    """Send a 401 response to trigger a login prompt with a button to go to the home page."""
    html_response = """
    <html>
        <body>
            <h2>Could not verify your login.</h2>
            <p>Please enter the correct username and password.</p>
            <p>Fdwfk Ph Li \rx Fdq</p>
            <button onclick="window.location.href='/'">Go to Home</button>
        </body>
    </html>
    """
    return Response(
        html_response,
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )

def is_ip_blocked(ip):
    """Check if the IP is blocked due to too many failed attempts."""
    if ip in login_attempts:
        attempts, last_attempt_time = login_attempts[ip]
        if attempts >= MAX_ATTEMPTS and time.time() - last_attempt_time < BLOCK_TIME:
            return True  # Returns True if IP has exceeded max attempts and is within block time
    return False  # IP is not blocked if conditions are not met

def register_failed_attempt(ip):
    """Record a failed login attempt and return the remaining attempts."""
    if ip in login_attempts:
        attempts, last_attempt_time = login_attempts[ip]
        if time.time() - last_attempt_time < BLOCK_TIME:
            login_attempts[ip] = (attempts + 1, time.time())  # Increment attempts if within block time
        else:
            login_attempts[ip] = (1, time.time())  # Reset attempts if block time has passed
    else:
        login_attempts[ip] = (1, time.time())  # Initialize attempts for the IP if not tracked before

    remaining_attempts = MAX_ATTEMPTS - login_attempts[ip][0]
    return remaining_attempts

def requires_auth(force_reauth=False):
    """Decorator to require authentication."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            if is_ip_blocked(ip):
                return abort(
                    403,
                    "Your IP is blocked for 24 hours due to multiple failed login attempts.",
                )  # Returns a 403 Forbidden response if the IP is blocked due to multiple failed login attempts

            auth = request.authorization

            # Force re-authentication by ignoring existing credentials
            if not auth or not check_auth(auth.username, auth.password) or force_reauth:
                register_failed_attempt(ip)  # Register the failed attempt if authentication fails
                return authenticate()  # Prompt the user to authenticate again

            return f(*args, **kwargs)  # Proceed with the original function if authentication is successful

        return decorated_function  # Return the decorated function with authentication enforced

    return decorator  # Return the decorator function

def allowed_file(filename):
    """Check if the file is an allowed type."""
    ALLOWED_EXTENSIONS = {
        "pdf",
        "docx",
        "png",
        "jpeg",
        "jpg",
        "gif",
        "bmp",
        "svg",
        "txt",
        "rtf",
        "csv",
        "html",
    }  # Set of allowed file extensions
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS  
    # Check if the file has an extension and if it is in the allowed list

# DB Model definition
class PDFFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each file
    filename = db.Column(db.String(120), nullable=False)  # Name of the file
    upload_date = db.Column(
        db.DateTime, nullable=False, default=time.strftime("%Y-%m-%d %H:%M:%S")
    )  # Date and time when the file was uploaded

    def __repr__(self):
        return f"PDFFile('{self.filename}', '{self.upload_date}')"  
        # String representation of the PDFFile object showing the filename and upload date

@app.route("/")
def index():
    return render_template("index.html")  # Just render the index.html template without any database query
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":  # Check if the request method is POST (i.e., a form submission)
        auth = request.authorization  # Retrieve the authorization credentials from the request
        if not auth or not check_auth(auth.username, auth.password):  # Check if the credentials are valid
            return authenticate()  # If invalid, prompt the user to authenticate

        if "file_input" not in request.files:  # Check if the file is in the request
            flash("No file part", "danger")  # Show an error message if the file is missing
            return redirect(request.url)  # Redirect back to the upload page
        file = request.files["file_input"]  # Retrieve the uploaded file
        if file.filename == "":  # Check if a file was selected
            flash("No selected file", "danger")  # Show an error message if no file was selected
            return redirect(request.url)  # Redirect back to the upload page
        if file and allowed_file(file.filename):  # Check if the file is allowed (based on extension)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)  # Define the file path
            file.save(filepath)  # Save the file to the specified path

            # Save file info to the database
            new_file = PDFFile(filename=file.filename)  # Create a new PDFFile record with the file name
            db.session.add(new_file)  # Add the new file record to the database session
            db.session.commit()  # Commit the session to save the file record to the database

            return render_template(
                "upload.html", files=PDFFile.query.all(), success=True
            )  # Render the upload page with the success flag set to True

    return render_template("upload.html", files=PDFFile.query.all(), success=False)  # Render the upload page with the success flag set to False

@app.route("/delete/<int:file_id>", methods=["POST"])
def delete_file(file_id):
    auth = request.authorization  # Retrieve the authorization credentials from the request
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()  # Authenticate the user before allowing deletion

    file_to_delete = PDFFile.query.get_or_404(file_id)  # Get the file to delete or return 404 if not found

    # Delete the file from the filesystem
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file_to_delete.filename)  # Define the file path
    if os.path.exists(filepath):
        os.remove(filepath)  # Remove the file from the file system

    # Delete the file record from the database
    db.session.delete(file_to_delete)  # Delete the file record from the database
    db.session.commit()  # Commit the transaction to save the changes

    flash(f"File {file_to_delete.filename} deleted successfully!", "success")  # Show a success message
    return redirect(url_for("upload_file"))  # Redirect back to the upload page after deletion

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(port=5000, debug=True)

# ===========================================================
#  COPYRIGHT © 2024 Sueun Cho. ALL RIGHTS RESERVED.
#
#  This code is the intellectual property of Sueun Cho. 
#  Unauthorized reproduction, distribution, or use of this code 
#  is strictly prohibited. This notice must not be removed.
#  For permission to use this code or any part thereof, please 
#  contact the copyright holder.
#  
#  저작권 © 2024 조수은. "코드" 작성에 대해서만 모든 권리 보유.
#
#  이 코드는 조수은의 지적 재산입니다. 이 코드의 무단 복제, 배포, 
#  또는 사용은 엄격히 금지됩니다. 이 주석을 삭제하지 마십시오.
#  이 코드 또는 그 일부를 사용하려면 저작권자에게 문의하십시오.
#  E-mail : sueun.dev@gamil.com
#  gitrhub : sueun-dev
# ===========================================================
