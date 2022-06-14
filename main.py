from sqlalchemy import Column, String, BigInteger, Boolean, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import database_exists, create_database
import random
import string

connectionstring = 'postgresql+psycopg2://postgres:example@postgres/newdatabase'
if not database_exists(connectionstring):  # => False
    try:
        create_database(connectionstring)
        doCreateAll = True
        print('Database created')
    except Exception as e:
        print('Database does not exists and cannot be created')
        raise
else:
    print('Database already exists')

engine = create_engine(connectionstring)

BaseModel = declarative_base()

unitedSequence = Sequence('id_seq')


# Struktury

Zamestnani_Skupiny = Table('zamestnani_skupiny', BaseModel.metadata,
                            Column('zamestnani_id', ForeignKey('zamestnani.id'),primary_key=True),
                            Column('studijniskupina_id', ForeignKey('studijniskupina.id'), primary_key=True),
                           )

Skupiny_Osoby = Table('skupiny_osoby', BaseModel.metadata,
                        Column('studijniskupina_id', ForeignKey('studijniskupina.id'), primary_key=True),
                        Column('osoba_id', ForeignKey('osoba,id'), primary_key=True),
                      )

class ZamestnaniModel(BaseModel):
    __tablename__= 'zamestnani'
    id =Column(BigInteger, Sequence('id_seq'), primary_key=True)
    id_skupiny = Column(BigInteger, ForeignKey('studijniskupina.id'))
    datum = Column(DateTime)

    pritomnosti = relationship('PritomnostModel', back_populates='zamestnane')

class StudijniSkupinaModel(BaseModel):
    __tablename__='studijniskupina'
    id = Column(BigInteger,Sequence('id_seq'), primary_key=True)
    nazev = Column(String)

class OsobaModel(BaseModel):
    __tablename__='osoba'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    jmeno = Column(String)
    prijmeni = Column(String)
    id_skupina = Column(BigInteger, ForeignKey('studijniskupina.id'))
    je_Student = Column(Boolean)

    pritomnost = relationship('PritomnostModel', back_populates='osoby')

class PritomnostModel(BaseModel):
    __tablename__ = 'pritomnost'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    id_zamestnani = Column(BigInteger, ForeignKey('zamestnani.id'))
    id_osoby = Column(BigInteger, ForeignKey('osoba.id'))
    pritomnost = Column(String)

    zamestnane = relationship('ZamestnaniModel', back_populates='pritomnosti')
    osoby = relationship('OsobaModel', back_populates='pritomnost')

#################################################################################

# Inicializase struktur
BaseModel.metadata.create_all(engine)

# Session

SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()
session.close()

session = SessionMaker()
session.close()
