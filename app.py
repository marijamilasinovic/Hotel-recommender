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
cursor = konekcija.cursor(dictionary=True, buffered=True)  # dictionary=True da bi se rezultati vraćali kao rečnici, buffered=True da bi se rezultati mogli ponovo koristiti

#Početna stranica
@app.route("/")
def index():
    cursor.execute("""SELECT hotel.hotelID, hotel.naziv, hotel.adresa, hotel.zvezdice, hotel.ljubimci, hotel.vrsta_smestaja, hotel.obrok,
                        grad.naziv_grada AS grad_naziv
                    FROM hotel
                    JOIN grad ON hotel.gradID = grad.gradID""")
    hoteli = cursor.fetchall()
    return render_template("hoteli.html", hoteli=hoteli)

#Dodavanje smestaja
@app.route("/dodaj_smestaj", methods=["GET", "POST"])
def dodaj_smestaj():
    if request.method == "GET":
        return render_template("dodaj_smestaj.html")

    naziv = request.form["naziv"]
    adresa = request.form["adresa"]
    grad = request.form["grad"]
    drzava = request.form["drzava"]
    kontinent = request.form["kontinent"]
    zvezdice = request.form["zvezdice"]
    ljubimci = request.form["ljubimci"]
    vrsta_smestaja = request.form["vrsta_smestaja"]
    obrok = request.form["obrok"]
    
    try:
        # 1) drzava
        cursor.execute("INSERT INTO drzava (drzava, kontinent) VALUES (%s, %s)", (drzava, kontinent))
        drzava_id = cursor.lastrowid
    
        # 2) grad
        cursor.execute("INSERT INTO grad (naziv_grada, drzavaID) VALUES (%s, %s)", (grad, drzava_id))
        grad_id = cursor.lastrowid
    
        # 3) hotel
        cursor.execute(
        "INSERT INTO hotel (naziv, adresa, gradID, zvezdice, ljubimci, vrsta_smestaja, obrok) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (naziv, adresa, grad_id, zvezdice, ljubimci, vrsta_smestaja, obrok)
        )
    
        konekcija.commit()
        return redirect(url_for("index"))
    except Exception:
        konekcija.rollback()
        raise

@app.route("/filter", methods=["GET", "POST"])
def filter():
    if request.method == "GET":
        return render_template("filter.html")

    zvezdice       = request.form.get("zvezdice")       or None
    ljubimci       = request.form.get("ljubimci")       or None
    vrsta_smestaja = request.form.get("vrsta_smestaja") or None
    obrok          = request.form.get("obrok")          or None

    query = """
        SELECT hotel.*, grad.naziv_grada AS grad_naziv
        FROM hotel
        JOIN grad ON hotel.gradID = grad.gradID
    """

    filters = []
    params = []

    if zvezdice:
        filters.append("hotel.zvezdice = %s")
        params.append(zvezdice)
    if ljubimci:
        filters.append("hotel.ljubimci = %s")
        params.append(ljubimci)
    if vrsta_smestaja:
        filters.append("hotel.vrsta_smestaja = %s")
        params.append(vrsta_smestaja)
    if obrok:
        filters.append("hotel.obrok = %s")
        params.append(obrok)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    cursor.execute(query, params)
    hoteli = cursor.fetchall()
    return render_template("hoteli.html", hoteli=hoteli)

if __name__ == "__main__":  # program startuje app.py
    app.run(debug = True)  # Promeniti na kraju projekta na False, da se ne bi prikazivali detalji o greškama korisnicima.