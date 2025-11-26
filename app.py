from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=os.getenv("MYSQLPORT")
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        ubicacion = request.form["ubicacion"]
        frecuencia = request.form["frecuencia"]
        potencia = request.form["potencia"]
        proveedor = request.form["proveedor"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO antenas (nombre, ubicacion, frecuencia, potencia, proveedor)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, ubicacion, frecuencia, potencia, proveedor))
        db.commit()

        return render_template("alert.html", mensaje="Antena registrada correctamente.")

    return render_template("register_antenna.html")

@app.route("/antenas")
def lista_antenas():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM antenas")
    data = cursor.fetchall()
    return render_template("antennas_list.html", antenas=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
