from flask import request, jsonify
from sc_server import app, db
from sc_server.models import Sastojak, Zaposleni, Korisnik, Proizvod

@app.route('/sastojak', methods=['GET'])
def get_all_sastojci():
    lista_sastojaka = Sastojak.query.all()
    sastojci = []

    for sastojak in lista_sastojaka:
       current_sastojak = {}
       current_sastojak['naziv'] = sastojak.naziv
       current_sastojak['jedinica'] = sastojak.jedinica
       sastojci.append(current_sastojak)

    return jsonify({'sastojci':sastojci})

@app.route('/sastojak', methods=['POST'])
def create_sastojak():
    data = request.get_json()
    s_naziv = data['naziv']
    s_jedinica = data['jedinica']

    lista_sastojaka = Sastojak.query.all()
    
    for sastojak in lista_sastojaka:
        if sastojak.naziv == s_naziv:
            return jsonify({'poruka':f'Sastojak vec postoji!'}), 409

    new_sastojak = Sastojak(naziv=s_naziv, jedinica=s_jedinica)
    
    db.session.add(new_sastojak)
    db.session.commit()

    return jsonify({'poruka':f'Sastojak <{s_naziv}> uspesno kreiran!'})

@app.route('/sastojak/<naziv>', methods=['DELETE'])
def delete_sastojak(naziv):
    sastojak = Sastojak.query.filter_by(naziv=naziv).first()

    if not sastojak:
        return jsonify({'poruka':'Sastojak nije pronadjen!'}), 409

    naziv = sastojak.naziv

    db.session.delete(sastojak)
    db.session.commit()

    return jsonify({'poruka':f'Sastojak <{naziv}> obrisan!'})

@app.route('/zaposleni', methods=['GET'])
def get_all_zaposleni():
    lista_zaposlenih = Zaposleni.query.all()
    zaposleni_to_send = []

    for zaposleni in lista_zaposlenih:
       current_zaposleni = {}
       current_zaposleni['ime'] = zaposleni.ime
       current_zaposleni['prezime'] = zaposleni.prezime
       current_zaposleni['JMBG'] = zaposleni.JMBG
       current_zaposleni['admin'] = zaposleni.admin
       zaposleni_to_send.append(current_zaposleni)

    return jsonify({'zaposleni':zaposleni_to_send})

@app.route('/zaposleni', methods=['POST'])
def create_zaposleni():
    data = request.get_json()
    z_ime = data['ime']
    z_prezime = data['prezime']
    z_JMBG = data['JMBG']
    
    try:
        z_admin = data['admin']
        new_zaposleni = Zaposleni(ime=z_ime, prezime=z_prezime, JMBG=z_JMBG, admin=z_admin) 
    except:
        new_zaposleni = Zaposleni(ime=z_ime, prezime=z_prezime, JMBG=z_JMBG)

    lista_zaposlenih = Zaposleni.query.all()

    for zaposleni in lista_zaposlenih:
        if zaposleni.JMBG == z_JMBG:
            return jsonify({'poruka':f'Zaposleni vec postoji!'}), 409
    
    db.session.add(new_zaposleni)
    db.session.commit()

    return jsonify({'poruka':f'Zaposleni <{z_ime} {z_prezime}> uspesno kreiran!'})

@app.route('/zaposleni/<JMBG>', methods=['DELETE'])
def delete_zaposleni(JMBG):
    zaposleni = Zaposleni.query.filter_by(JMBG=JMBG).first()

    if not zaposleni:
        return jsonify({'poruka':'Zaposleni nije pronadjen!'}), 409

    ime = zaposleni.ime
    prezime = zaposleni.prezime

    db.session.delete(zaposleni)
    db.session.commit()

    return jsonify({'poruka':f'Zaposleni <{ime} {prezime}> obrisan!'})

@app.route('/korisnik', methods=['GET'])
def get_all_korisnici():
    lista_korisnika = Korisnik.query.all()
    korisnici = []

    for korisnik in lista_korisnika:
       current_korisnik = {}
       current_korisnik['email'] = korisnik.email
       korisnici.append(current_korisnik)

    return jsonify({'korisnici':korisnici})

@app.route('/korisnik', methods=['POST'])
def create_korisnik():
    data = request.get_json()
    k_email = data['email']
    k_lozinka = data['lozinka']
    
    lista_korisnika = Korisnik.query.all()

    new_korisnik = Korisnik(email=k_email, lozinka=k_lozinka)

    for korisnik in lista_korisnika:
        if korisnik.email == k_email:
            return jsonify({'poruka':f'Email vec postoji!'}), 409
    
    db.session.add(new_korisnik)
    db.session.commit()

    return jsonify({'poruka':f'Korisnik <{k_email}> uspesno kreiran!'})

@app.route('/korisnik/<email>', methods=['DELETE'])
def delete_korisnik(email):
    korisnik = Korisnik.query.filter_by(email=email).first()

    if not korisnik:
        return jsonify({'poruka':'Brisanje neuspesno!'}), 409

    email = korisnik.email

    db.session.delete(korisnik)
    db.session.commit()

    return jsonify({'poruka':f'Korisnik <{email}> obrisan!'})

@app.route('/proizvod', methods=['GET'])
def get_all_proizvodi():
    lista_proizvoda = Proizvod.query.all()
    proizvodi = []
    
    for proizvod in lista_proizvoda:
        current_proizvod = {}
        current_proizvod['naziv'] = proizvod.naziv
        current_proizvod['cena'] = proizvod.cena
        current_proizvod['tip'] = proizvod.tip
        current_proizvod['slika'] = proizvod.slika
        current_proizvod['sastojci'] = []

        for asoc in proizvod.sastojci:
            current_sastojak = {}
            current_sastojak['naziv'] = asoc.sastojak.naziv
            current_sastojak['jedinica'] = asoc.sastojak.jedinica
            current_sastojak['kolicina'] = asoc.kolicina

            current_proizvod['sastojci'].append(current_sastojak)
        
        proizvodi.append(current_proizvod)

    return jsonify({'proizvodi':proizvodi})
