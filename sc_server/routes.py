from flask import request, jsonify
from sc_server import app, db
from sc_server.models import Sastojak, Zaposleni

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
        if (sastojak.naziv == s_naziv and sastojak.jedinica == s_jedinica):
            return jsonify({'poruka':f'Sastojak vec postoji!'}), 409

    new_sastojak = Sastojak(naziv=s_naziv, jedinica=s_jedinica)
    
    db.session.add(new_sastojak)
    db.session.commit()

    return jsonify({'poruka':f'Sastojak <{s_naziv}> uspesno kreiran!'})

@app.route('/sastojak/<id>', methods=['DELETE'])
def delete_sastojak(id):
    sastojak = Sastojak.query.filter_by(id=id).first()

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

    return jsonify({'poruka':f'zaposleni <{ime} {prezime}> obrisan!'})