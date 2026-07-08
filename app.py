from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    connection = sqlite3.connect("guestbook.db")
    connection.execute("CREATE TABLE IF NOT EXISTS entries (name TEXT, message TEXT)")
    connection.close()

@app.route("/", methods=["GET", "POST"])
def home():
    connection = sqlite3.connect("guestbook.db")

    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        connection.execute("INSERT INTO entries (name, message) VALUES (?, ?)", (name, message))
        connection.commit()
        connection.close()
        return redirect("/")

    entries = connection.execute("SELECT name, message FROM entries").fetchall()
    connection.close()
    return render_template("index.html", entries=entries)

init_db()

