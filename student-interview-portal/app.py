import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import boto3
import pymysql
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-in-production")

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def get_db():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=int(os.getenv("DB_PORT", "3306")),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_s3():
    return boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()
        password = request.form["password"]

        if not all([name, email, phone, password]):
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        try:
            db = get_db()
            with db.cursor() as cur:
                cur.execute(
                    "INSERT INTO students (name, email, phone, password_hash) VALUES (%s,%s,%s,%s)",
                    (name, email, phone, password_hash)
                )
            db.close()
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))
        except pymysql.err.IntegrityError:
            flash("Email already registered.", "danger")
        except Exception as e:
            app.logger.exception(e)
            flash("Registration failed.", "danger")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        db = get_db()
        with db.cursor() as cur:
            cur.execute("SELECT * FROM students WHERE email=%s", (email,))
            user = cur.fetchone()
        db.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        resume = request.files.get("resume")

        if not resume or not resume.filename:
            flash("Please select a resume.", "danger")
            return redirect(url_for("dashboard"))

        if not allowed_file(resume.filename):
            flash("Only PDF, DOC and DOCX files are allowed.", "danger")
            return redirect(url_for("dashboard"))

        resume.seek(0, os.SEEK_END)
        size = resume.tell()
        resume.seek(0)

        if size > MAX_FILE_SIZE:
            flash("Resume must be 5 MB or smaller.", "danger")
            return redirect(url_for("dashboard"))

        extension = resume.filename.rsplit(".", 1)[1].lower()
        object_key = f"resumes/{session['user_id']}/{uuid.uuid4()}.{extension}"

        try:
            s3 = get_s3()
            s3.upload_fileobj(
                resume,
                os.environ["S3_BUCKET"],
                object_key,
                ExtraArgs={"ContentType": resume.content_type or "application/octet-stream"}
            )

            db = get_db()
            with db.cursor() as cur:
                cur.execute(
                    "UPDATE students SET resume_s3_key=%s, resume_original_name=%s WHERE id=%s",
                    (object_key, resume.filename, session["user_id"])
                )
            db.close()

            flash("Resume uploaded successfully to S3.", "success")
        except ClientError:
            app.logger.exception("S3 upload failed")
            flash("S3 upload failed. Check IAM permissions and bucket configuration.", "danger")
        except Exception as e:
            app.logger.exception(e)
            flash("Upload failed.", "danger")

        return redirect(url_for("dashboard"))

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "SELECT name, email, phone, resume_original_name FROM students WHERE id=%s",
            (session["user_id"],)
        )
        user = cur.fetchone()
    db.close()

    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
