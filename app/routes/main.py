import os
from datetime import datetime, timedelta
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify,
    send_from_directory,
    Response,
)
from werkzeug.utils import secure_filename

# Relative imports to match your package structure
from .. import db
from ..models import PDFFile
from ..config import Config
from ..decorators import check_auth, authenticate
from ..utils import allowed_file

bp = Blueprint("main", __name__)

if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

        if "file_input" not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)

        file = request.files["file_input"]
        # 1. Ensure we handle 'None' or empty filename
        raw_filename = file.filename or ""
        if not raw_filename:
            flash("No selected file", "danger")
            return redirect(request.url)

        # 2. Check extension, then use secure_filename
        if file and allowed_file(raw_filename):
            filename = secure_filename(raw_filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)

            # 3. If your model has an __init__(filename: str)
            new_file = PDFFile(filename=filename)
            db.session.add(new_file)
            db.session.commit()

            files = PDFFile.query.order_by(PDFFile.upload_date.desc()).all()
            # Mark files as 'new' if uploaded within 7 days
            for f in files:
                f.is_new = (datetime.utcnow() - f.upload_date) <= timedelta(days=7)
            return render_template("upload.html", files=files, success=True)

    # Handle GET request
    files = PDFFile.query.order_by(PDFFile.upload_date.desc()).all()
    for f in files:
        f.is_new = (datetime.utcnow() - f.upload_date) <= timedelta(days=7)
    return render_template("upload.html", files=files, success=False)


@bp.route("/delete/<int:file_id>", methods=["POST"])
def delete_file(file_id):
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    file_to_delete = PDFFile.query.get_or_404(file_id)
    filepath = os.path.join(Config.UPLOAD_FOLDER, file_to_delete.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(file_to_delete)
    db.session.commit()

    flash(f"File {file_to_delete.filename} deleted successfully!", "success")
    return redirect(url_for("main.upload_file"))


@bp.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@bp.errorhandler(500)
def internal_error(error):
    return render_template("404.html"), 500


@bp.route("/api")
def api():
    files = PDFFile.query.order_by(PDFFile.upload_date.desc()).all()
    file_list = [
        {
            "id": f.id,
            "filename": f.filename,
            "upload_date": f.upload_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for f in files
    ]
    return jsonify(file_list)


@bp.route("/robots.txt")
def robots_txt():
    lines = ["User-agent: *", "Allow: /", "Sitemap: https://umdkusa.com/sitemap.xml"]
    return Response("\n".join(lines), mimetype="text/plain")
