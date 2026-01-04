from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="system_ocen",
    user="postgres",
    password="1234",
     options="-c client_encoding=UTF8",
     port=5432
)

@app.route("/")
def index():
    cur = conn.cursor()
    cur.execute("""
        SELECT u.imie, u.nazwisko, p.nazwa, o.ocena, o.data_oceny
        FROM oceny o
        JOIN uczniowie u ON o.uczen_id = u.id
        JOIN przedmioty p ON o.przedmiot_id = p.id
        ORDER BY o.data_oceny DESC
    """)
    oceny = cur.fetchall()
    cur.close()
    return render_template("index.html", oceny=oceny)

@app.route("/dodaj", methods=["GET", "POST"])
def dodaj_ocene():
    if request.method == "POST":
        uczen_id = request.form["uczen_id"]
        przedmiot_id = request.form["przedmiot_id"]
        ocena = request.form["ocena"]

        cur = conn.cursor()
        cur.execute(
            "INSERT INTO oceny (uczen_id, przedmiot_id, ocena) VALUES (%s, %s, %s)",
            (uczen_id, przedmiot_id, ocena)
        )
        conn.commit()
        cur.close()
        return redirect("/")

    return render_template("dodaj_ocene.html")

if __name__ == "__main__":
    app.run(debug=True)
