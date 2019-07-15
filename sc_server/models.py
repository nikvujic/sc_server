from sc_server import db
from datetime import datetime

class Racun(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    sto = db.Column(db.Integer, nullable=False)
    datum = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    korisnikID = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)
    zaposleniID = db.Column(db.Integer, db.ForeignKey('zaposleni.id'), nullable=False)

    def __repr__(self):
        return f"Racun('{self.sto}', '{self.datum}')"

sastojci_proizvoda = db.Table('sastojci_proizvoda',
    db.Column('sastojak_id', db.Integer, db.ForeignKey('sastojak.id')),
    db.Column('proizvod_id', db.Integer, db.ForeignKey('proizvod.id'))
)

stavke_racuna = db.Table('stavke_racuna',
    db.Column('proizvod_id', db.Integer, db.ForeignKey('proizvod.id')),
    db.Column('racun_id', db.Integer, db.ForeignKey('racun.id'))
)

class Sastojak(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(50), unique=True, nullable=False)
    kolicina = db.Column(db.Integer, nullable=False)
    jedinica = db.Column(db.String(20), nullable=False)
    u_proizvodima = db.relationship('Proizvod', secondary=sastojci_proizvoda, backref=db.backref('sastojci', lazy='dynamic'))

    def __repr__(self):
        return f"Sastojak('{self.naziv}', '{self.kolicina}', '{self.jedinica}')"

class Korisnik(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    lozinka = db.Column(db.String(60), nullable=False)
    racuni = db.relationship('Racun', backref='uplatio', lazy=True)

    def __repr__(self):
        return f"Korisnik('{self.email}', '{self.lozinka}')"

class Zaposleni(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(30), nullable=False)
    prezime = db.Column(db.String(30), nullable=False)
    JMBG = db.Column(db.String(20), unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    racuni = db.relationship('Racun', backref='naplatio', lazy=True)

    def __repr__(self):
        return f"Zaposleni('{self.ime}', '{self.prezime}', '{self.JMBG}', '{self.admin}')"

class Proizvod(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(50), unique=True, nullable=False)
    cena = db.Column(db.Float, nullable=False)
    tip = db.Column(db.String(25), nullable=False)
    slika = db.Column(db.String(20), nullable=True)
    na_racunima = db.relationship('Racun', secondary=stavke_racuna, backref=db.backref('proizvodi', lazy='dynamic'))

    def __repr__(self):
        return f"Proizvod('{self.naziv}', '{self.cena}', '{self.tip}')"
