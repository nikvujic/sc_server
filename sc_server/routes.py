from flask import request, jsonify
from sc_server import app, db
from sc_server.models import Sastojak

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
    naziv = sastojak.naziv

    if not sastojak:
        return jsonify({'poruka':'Sastojak nije pronadjen!'})

    db.session.delete(sastojak)
    db.session.commit()

    return jsonify({'poruka':f'Sastojak <{naziv}> obrisan!'})