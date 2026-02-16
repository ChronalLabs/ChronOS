from flask import Flask, render_template, request
import sqlite3
from utils.calculator import calculate_total

app = Flask(__name__)

DATABASE = "carbon.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            travel REAL,
            electricity REAL,
            diet REAL,
            total REAL,
            yearly REAL,
            score INTEGER,
            category TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/result", methods=["POST"])
def result():

    data = request.form

    # Calculate everything from calculator.py
    result_data = calculate_total(data)

    # Save to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history (travel, electricity, diet, total, yearly, score, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        result_data["travel"],
        result_data["electricity"],
        result_data["diet"],
        result_data["total"],
        result_data["yearly"],
        result_data["score"],
        result_data["category"]
    ))

    conn.commit()
    conn.close()

    return render_template("result.html", result=result_data)


@app.route("/history")
def history():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    records = cursor.fetchall()

    conn.close()

    return render_template("history.html", data=records)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
