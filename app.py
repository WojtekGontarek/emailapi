import datetime

from flask import Flask, render_template, request, session, redirect
import requests

app = Flask(__name__)
app.secret_key = "kabaczek"

API_KEY = open("apiKey.txt", "r").read()

API_URL = "https://identitytoolkit.googleapis.com/v1/accounts"

DB_URL = "https://console.firebase.google.com/u/1/project/flaskproject-c9d74/database/flaskproject-c9d74-default-rtdb/data/~2F"

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/profile")
    else:
        return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]

    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(f"{API_URL}:signUp?key={API_KEY}",
                             json=payload)

    if response.status_code == 200:
        session["user_id"] = response.json()["localId"]
        return redirect("/profile")
    else:
        return render_template("index.html", error=response.json()["error"]["message"])


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    print(email)
    print(request.form.get("email"))
    password = request.form["password"]

    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(
        f"{API_URL}:signInWithPassword?key={API_KEY}", json=payload)

    if response.status_code == 200:
        session["user_id"] = response.json()["localId"]
        print(response.json())
        return redirect("/profile")
    else:
        return render_template("index.html", error="Invalid email or password")


@app.route("/profile")
def profile():
    if "user_id" in session:
        return render_template("profile.html")
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

# def get_user_notes(user_id):
#     db_path = f"notes/{user_id}"
#     response = requests.get(f"{DB_URL}/{db_path}.json")
#     if response.status_code == 200:
#         return response.json() or {}
#     else:
#         return {}

# @app.route("/create_note", methods=["POST"])
# def create_note(user_id, note_title, note_body):
#     db_path = f"notes/{user_id}"
#
#     res = requests.post(f"{DB_URL}/{db_path}.json", json={
#         'title': note_title,
#         'body': note_body,
#         'created_at': str(datetime.datetime.now())
#     }).json()['name']
#
#     return res


if __name__ == '__main__':
    app.run(debug=True)
