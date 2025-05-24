from flask import Flask
from flask import url_for, redirect, render_template, request, session
from datetime import timedelta
import auth
import secret

app = Flask(__name__)
app.secret_key = secret.session_secret_key() # for session encryptoin
app.permanent_session_lifetime = timedelta(minutes=10) # session should stay active for only 10 minusts if not in use

@app.route("/login/", methods=['GET', 'POST'])
def login():
    """
    - Render 'login template
    - Initiate session
    - Receive POST request from user
    - Redirect to home page'
    """
    if request.method == 'POST': # when the form is submited
        user_email = request.form.get("user_email") # return the email data from the form
        user_password = request.form.get("user_password") # return the password data from the form

        # check the credatials in the database
        username_status, username = auth.auth_login(user_email, user_password)

        if username_status:
            # create user session
            session["user"] = username
            # redirect to home page
            return redirect(url_for('home', username=session["user"])) #url for takes the function name
        
        else: return render_template("login.html")

    else: return render_template("login.html")

@app.route("/<username>")
@app.route("/home/<username>")
def home(username):
    # if the user is found in session data values then go to home page
    if "user" in session:
        return render_template("home.html", username=session["user"])
    else: return redirect(url_for("login")) # stay at the home screen

@app.route("/students/")
def students():
    pass

@app.route("/courses/")
def courses():
    pass

@app.route("/teachers/")
def teachers():
    pass

@app.route("/logout/")
def logout():
    """
    - Logout by killing the session state
    - redirect to home screen
    """
    # when the user logs out, the remvoe the session data and quit
    session.pop("user", None)
    return redirect(url_for("login"))

@app.after_request
def add_header(response):
    """
    This helps stop the browser from showing the "home" page if someone presses the back button after logout.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == "__main__":
    app.run(debug=True)