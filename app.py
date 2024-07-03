from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("C:/dev/new/Cloud Chat/db.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS message (id integer primary key, name tinytext, content tinytext, created_at timestamp default current_timestamp)")
con.close()

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        return redirect(f"/{username.lower()}")
    return render_template("index.html")

@app.route("/<name>", methods=["GET", "POST"])
def chat(name):

    name = str(name).lower()

    con = sqlite3.connect("C:/dev/new/Cloud Chat/db.db")
    cur = con.cursor()

    if request.method == "POST":
        content = request.form["msg"]
        cur.execute(f"INSERT INTO message (name, content) VALUES ('{name}', '{content}') ")
        con.commit()
    
    cur.execute("SELECT * FROM message ORDER BY created_at")
    messages = cur.fetchall()

    return render_template("chat.html", messages=messages, name=name)

app.run(debug=True, port=5000, host="0.0.0.0")