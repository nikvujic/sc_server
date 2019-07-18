from flask import request, jsonify
from sc_server import app, db
from sc_server.models import Sastojak

@app.route('/sastojak', methods=['POST'])
def napravi_sastojak():
    data = request.get_json()
    s_naziv = data['naziv']
    s_jedinica = data['jedinica']

    same_name_sastojci = Sastojak.query.all()

    for sastojak in same_name_sastojci:
        if (sastojak.naziv == s_naziv and sastojak.jedinica == s_jedinica):
            return jsonify({'poruka':f'Sastojak vec postoji!'}), 409

    new_sastojak = Sastojak(naziv=s_naziv, jedinica=s_jedinica)
    
    db.session.add(new_sastojak)
    db.session.commit()

    return jsonify({'poruka':f'Sastojak {s_naziv} uspesno kreiran!'})