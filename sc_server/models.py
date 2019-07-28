from sc_server import db
from datetime import datetime

class Racun(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    sto = db.Column(db.Integer, nullable=False)
    public_id = db.Column(db.String(50), unique=True)
    datum = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    korisnikID = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)
    zaposleniID = db.Column(db.Integer, db.ForeignKey('zaposleni.id'), nullable=False)
    proizvodi = db.relationship("Stavke_Racuna", back_populates="racun", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Racun('{self.sto}', '{self.datum}')"

class Proizvod(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(50), unique=True, nullable=False)
    cena = db.Column(db.Float, nullable=False)
    tip = db.Column(db.String(25), nullable=False)
    slika = db.Column(db.String(20), nullable=True)
    racuni = db.relationship("Stavke_Racuna", back_populates="proizvod")
    sastojci = db.relationship("Sastojci_Proizvoda", back_populates="proizvod", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Proizvod('{self.naziv}', '{self.cena}', '{self.tip}')"

# ovo je tabela asocijacije
class Sastojci_Proizvoda(db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'sastojci_proizvoda'
    sastojak_id = db.Column(db.Integer, db.ForeignKey('sastojak.id'), primary_key=True)
    proizvod_id = db.Column(db.Integer, db.ForeignKey('proizvod.id'), primary_key=True)
    kolicina = db.Column(db.Integer, nullable=False, default=1)
    sastojak = db.relationship("Sastojak", back_populates='proizvodi')
    proizvod = db.relationship("Proizvod", back_populates='sastojci')

# ovo je tabela asocijacije
class Stavke_Racuna(db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'stavke_racuna'
    proizvod_id = db.Column(db.Integer, db.ForeignKey('proizvod.id'), primary_key=True)
    racun_id = db.Column(db.Integer, db.ForeignKey('racun.id'), primary_key=True)
    kolicina = db.Column(db.Integer, nullable=False, default=1)
    proizvod = db.relationship("Proizvod", back_populates='racuni')
    racun = db.relationship("Racun", back_populates='proizvodi')

class Sastojak(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(50), unique=True, nullable=False)
    jedinica = db.Column(db.String(20), nullable=False)
    proizvodi = db.relationship("Sastojci_Proizvoda", back_populates="sastojak")

    def __repr__(self):
        return f"Sastojak('{self.naziv}', '{self.jedinica}')"

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
    lozinka = db.Column(db.String(60), nullable=False)
    JMBG = db.Column(db.String(20), unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    racuni = db.relationship('Racun', backref='naplatio', lazy=True)

    def __repr__(self):
        return f"Zaposleni('{self.ime}', '{self.prezime}', '{self.lozinka}', '{self.JMBG}', '{self.admin}')"
