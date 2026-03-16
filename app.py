from flask import Flask, render_template, request, redirect, url_for

import mysql.connector

app = Flask(__name__) # rutina za kreiranje aplikacije

# konekcija na bazu

konekcija = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="smestaj"
)
cursor = konekcija.cursor(dictionary=True)

#Početna stranica
@app.route("/")
def index():
    cursor.execute("SELECT * FROM hotel")
    hotel = cursor.fetchall()
    return render_template("index.html", hotel=hotel)

#upisivanje države
@app.route("/dodaj_drzavu", methods=["GET", "POST"])
def dodaj_drzavu():
    if request.method == "POST":
        naziv = request.form["naziv"]
        kontinent = request.form["kontinent"]
        cursor.execute("INSERT INTO drzava (naziv, kontinent) VALUES (%s, %s)", (naziv, kontinent))
        konekcija.commit()
        return redirect(url_for("index"))
    return render_template("dodaj_drzavu.html")

#upisivanje grada
@app.route("/dodaj_grad", methods=["GET", "POST"])
def dodaj_grad():
    if request.method == "POST":
        naziv = request.form["naziv"]
        drzava_id = request.form["drzava_id"]
        cursor.execute("INSERT INTO grad (naziv, drzava_id) VALUES (%s, %s)", (naziv, drzava_id))
        konekcija.commit()
        return redirect(url_for("index"))
    cursor.execute("SELECT * FROM drzava")
    drzava = cursor.fetchall()
    return render_template("dodaj_grad.html", drzava=drzava)

#upisivanje hotela
@app.route("/dodaj_hotel", methods=["GET", "POST"])
def dodaj_hotel():
    if request.method == "POST":
        naziv = request.form["naziv"]
        grad_id = request.form["grad_id"]
        adresa = request.form["adresa"]
        zvezdice = request.form["zvezdice"]
        ljubimci = request.form.get("ljubimci", "ne")
        vrsta_smestaja = request.form["vrsta_smestaja"]
        obrok = request.form["obrok"]
        cursor.execute("INSERT INTO hotel (naziv, adresa, grad_id, zvezdice, ljubimci, vrsta_smestaja, obrok) VALUES (%s, %s, %s, %s, %s, %s, %s)", (naziv, adresa, grad_id, zvezdice, ljubimci, vrsta_smestaja, obrok))
        konekcija.commit()
        return redirect(url_for("index"))
    cursor.execute("SELECT * FROM grad")
    grad = cursor.fetchall()
    return render_template("dodaj_hotel.html", grad=grad)

if __name__ == "__main__":  # program startuje app.py
    app.run(debug = True)  # Promeniti na kraju projekta na False, da se ne bi prikazivali detalji o greškama korisnicima.