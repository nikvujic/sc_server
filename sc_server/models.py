from sc_server import db
from datetime import datetime

class Sastojak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(50), unique=True, nullable=False)
    kolicina = db.Column(db.Integer, nullable=False)
    jedinica = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Sastojak('{self.naziv}', '{self.kolicina}', '{self.jedinica}')"

class Korisnik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Korisnik('{self.email}', '{self.password}')"

class Zaposleni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Columnt(db.String(30), nullable=False)
    prezime = db.Column(db.String(30), nullable=False)
    JMBG = db.Column(db.String(20), unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Zaposleni('{self.ime}', '{self.prezime}', '{self.JMBG}', '{self.admin}')"

class Proizvod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(50), unique=True, nullable=False)
    cena = db.Column(db.Float, nullable=False)
    tip = db.Column(db.String(25), nullable=False)
    slika = db.Column(db.String(20), nullable=True)
    sastojci = db.relationship('Sastojak', backref='sadrzi', lazy=True)

    def __repr__(self):
        return f"Proizvod('{self.naziv}', '{self.cena}', '{self.tip}')"

class Racun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sto = db.Column(db.Integer, nullable=False)
    datum = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    proizvodi = db.relationship('Proizvod', backref='ima', lazy=True)
    korisnikID = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)
    zaposleniID = db.Column(db.Integer, db.ForeignKey('zaposleni.id'), nullable=False)

    def __repr__(self):
        return f"Racun('{self.sto}', '{self.datum}')"