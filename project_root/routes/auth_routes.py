from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.student import Student
from models import db

auth_bp = Blueprint("auth", __name__)

# ---------------- LOGIN PAGE ----------------
@auth_bp.route("/", methods=["GET"])
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# ---------------- LOGIN LOGIC ----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")

    if not email:
        flash("Email is required", "error")
        return redirect(url_for("auth.login_page"))

    student = Student.query.filter_by(email=email).first()

    if not student:
        flash("Account not found. Please sign up.", "error")
        return redirect(url_for("auth.signup_page"))

    session["student_id"] = student.id
    return redirect(url_for("student.dashboard"))


# ---------------- SIGNUP PAGE ----------------
@auth_bp.route("/signup", methods=["GET"])
def signup_page():
    return render_template("sign_up.html")


# ---------------- SIGNUP LOGIC ----------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        flash("All fields are required", "error")
        return redirect(url_for("auth.signup_page"))

    if Student.query.filter_by(email=email).first():
        flash("Email already exists. Please login.", "error")
        return redirect(url_for("auth.login_page"))

    student = Student(name=name, email=email)
    db.session.add(student)
    db.session.commit()

    session["student_id"] = student.id
    return redirect(url_for("student.dashboard"))


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))
