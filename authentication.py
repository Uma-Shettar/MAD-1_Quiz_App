from app import app
from flask import render_template, request, redirect, url_for, flash, session
from database import *
from datetime import datetime
from routes import *

@app.route("/login" , methods = ["GET","POST"])
def login():
    if request.method == "GET":
        if 'user_email' in session:
            return redirect(url_for("home"))
        return render_template("login.html")
    
    if request.method == "POST":
        email = request.form.get("email",None)
        password = request.form.get("password",None)
        
        if not email:
            flash("Email is required")
            return redirect(url_for("login"))
        
        if not password:  
            flash("Password is required")
            return redirect(url_for("login"))
        
        if "@" not in email:
            flash("Invalid Email")
            return redirect(url_for("login"))
        
        user = User.query.filter_by(user_email = email).first()
        if not user:
            flash("User not found...  Please register......")
            return redirect(url_for("register"))
        
        if user.password != password:
            flash("Invalid Password")
            return redirect(url_for("login"))
        
        session["user_email"] = user.user_email
        session["user_role"] = user.role

        flash("...Login Successful...")
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    if 'user_email' not in session:
        flash("You haven't logged in yet")
        return redirect(url_for("login"))
    
    session.pop("user_email")
    session.pop("user_role")
    if 'target_time' in session:
        session.pop("target_time")

    flash("...Logged out successfully...")
    return redirect(url_for("login"))

@app.route("/register" , methods = ["GET","POST"])
def register():
    if request.method == "GET":
        if 'user_email' in session:
            return redirect(url_for("home"))
        return render_template("register.html")
    
    if request.method == "POST":
        email = request.form.get("email",None)
        password = request.form.get("password",None)
        confirm_password = request.form.get("confirm_password",None)
        username = request.form.get("username",None)   
        qualification = request.form.get("qualification",None)
        dob = request.form.get("dob",None)
        role = "user"

        if not email:
            flash("Email is required")
            return redirect(url_for("register"))
        
        if not password:
            flash("Password is required")  
            return redirect(url_for("register"))
        
        if '@' not in email:
            flash("Invalid Email")
            return redirect(url_for("register"))
        
        if not username:
            flash("Username is required")
            return redirect(url_for("register"))
        
        if not qualification:
            flash("Qualification is required")
            return redirect(url_for("register"))
        if not dob:
            flash("Date of Birth is required")
            return redirect(url_for("register"))
        if not confirm_password:
            flash("Confirm the password")
            return redirect(url_for("register"))
        
        if password != confirm_password:
            flash("Password and Confirm Password should match") 
            return redirect(url_for("register"))
        
        if len(password) < 8:
            flash("Password should be at least 8 characters long")
            return redirect(url_for("register"))
        
        user = User.query.filter_by(user_email = email).first()
        if user:
            flash("User already exists... Please login or use another email....")
            return redirect(url_for("login"))
        
        user = User(
            user_email = email, 
            password = password, 
            username = username, 
            qualification = qualification, 
            dob = datetime.strptime(dob, "%Y-%m-%d"),
            role = role
        )

        db.session.add(user)
        db.session.commit()

        flash("...Registration Successful...")

        return redirect(url_for("login"))
        
