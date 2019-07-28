from flask import request, jsonify
from sc_server import app, db
from sc_server.models import (Sastojak, Zaposleni, Korisnik,
    Proizvod, Sastojci_Proizvoda, Racun, Stavke_Racuna)
from werkzeug.security import generate_password_hash
import uuid

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

@app.route('/zaposleni/promote/<JMBG>', methods=['PUT'])
def promote_zaposleni(JMBG):
    zaposleni = Zaposleni.query.filter_by(JMBG=JMBG).first()

    ime = zaposleni.ime
    prezime = zaposleni.prezime

    if not zaposleni:
        return jsonify({'poruka':'Zaposleni nije pronadjen!'}), 409
    
    zaposleni.admin = request.get_json()['admin']
    db.session.commit()

    return jsonify({'poruka':f'Zaposlenom <{ime} {prezime}> promenjen pristup!'})

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
    hash_pass = generate_password_hash(k_lozinka, method='sha256')

    new_korisnik = Korisnik(email=k_email, lozinka=hash_pass)

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

@app.route('/proizvod', methods=['POST'])
def create_proizod():
    data = request.get_json()
    p_naziv = data['naziv']
    p_cena = data['cena']
    p_tip = data['tip']
    p_sastojci = data['sastojci']

    proizvod = Proizvod(naziv=p_naziv, cena=p_cena, tip=p_tip)

    for item in p_sastojci:
        current_sastojak = Sastojak.query.filter_by(naziv=item['naziv']).first()
        asoc = Sastojci_Proizvoda(kolicina=item['kolicina'])
        asoc.sastojak = current_sastojak
        proizvod.sastojci.append(asoc)

    db.session.add(proizvod)
    db.session.commit()

    return jsonify({'poruka':f'Proizvod <{p_naziv}> uspesno kreiran!'})
    

@app.route('/proizvod/<naziv>', methods=['DELETE'])
def delete_proizvod(naziv):
    proizvod = Proizvod.query.filter_by(naziv=naziv).first()

    if not proizvod:
        return jsonify({'poruka':'Brisanje neuspesno!'}), 409

    naziv = proizvod.naziv

    proizvod.sastojci.clear()

    db.session.delete(proizvod)
    db.session.commit()

    return jsonify({'poruka':f'Proizvod <{naziv}> obrisan!'})

@app.route('/racun', methods=['GET'])
def get_all_racuni():
    lista_racuna = Racun.query.all()
    racuni = []
    
    for racun in lista_racuna:
        current_racun = {}
        current_racun['sto'] = racun.sto
        current_racun['public_id'] = racun.public_id
        current_racun['korisnikID'] = racun.korisnikID
        current_racun['zaposleniID'] = racun.zaposleniID
        current_racun['datum'] = racun.datum
        current_racun['proizvodi'] = []

        for asoc in racun.proizvodi:
            current_proizvod = {}
            current_proizvod['naziv'] = asoc.proizvod.naziv
            current_proizvod['kolicina'] = asoc.kolicina
            current_proizvod['cena'] = asoc.proizvod.cena

            current_racun['proizvodi'].append(current_proizvod)
        
        racuni.append(current_racun)

    return jsonify({'racuni':racuni})

@app.route('/racun', methods=['POST'])
def create_racun():
    data = request.get_json()
    r_sto = data['sto']
    r_zaposleni = data['zaposleni']
    r_korisnik = data['korisnik']
    r_proizvodi = data['proizvodi']

    racun = Racun(sto=r_sto, public_id=str(uuid.uuid4()), korisnikID=r_korisnik, zaposleniID=r_zaposleni)

    for item in r_proizvodi:
        current_proizvod = Proizvod.query.filter_by(naziv=item['naziv']).first()
        asoc = Stavke_Racuna(kolicina = item['kolicina'])
        asoc.proizvod = current_proizvod
        racun.proizvodi.append(asoc)

    db.session.add(racun)
    db.session.commit()

    return jsonify({'poruka':f'Racun uspesno kreiran!'})

@app.route('/racun/<public_id>', methods=['DELETE'])
def delete_racun(public_id):
    racun = Racun.query.filter_by(public_id=public_id).first()

    if not racun:
        return jsonify({'poruka':'Brisanje neuspesno!'}), 409
    
    racun.proizvodi.clear()

    db.session.delete(racun)
    db.session.commit()

    return jsonify({'poruka':f'Racun obrisan!'})