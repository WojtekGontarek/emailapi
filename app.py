from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import requests

app = Flask(__name__)

API_URL = "https://reqres.in/api"
app.secret_key = 'super secret key'


@app.route("/")
def index():
    if "token" in session:
        return redirect("/users")
    else:
        return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    print(email)
    print(request.form.get("email"))
    password = request.form["password"]

    # Simulate basic authentication
    payload = {"email": email, "password": password}

    # Send POST request to authenticate user
    response = requests.post(f"{API_URL}/login", data=payload)

    # Check if authentication is successful
    if response.status_code == 200:
        session["token"] = response.json()["token"]
        return redirect("/users")
    else:
        return render_template("index.html", error="Invalid email or password")


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]

    # Simulate user registration
    payload = {"email": email, "password": password}

    # Send POST request to register user
    response = requests.post(f"{API_URL}/register", data=payload)
    print(response.json())
    print(response.status_code)
    # Check if registration is successful
    if response.status_code == 200:
        session["token"] = response.json()["token"]
        return redirect("/users")
    else:
        return render_template("index.html", error=response.json().get("error"))


@app.route("/users")
def users():
    if "token" in session:
        # Fetch users from ReqRes.in API
        headers = {"Authorization": f"Bearer {session['token']}"}
        response = requests.get(f"{API_URL}/users", headers=headers)
        users = response.json()["data"]

        return render_template("users.html", users=users)
    else:
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    # Remove token from session
    session.pop("token", None)
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
