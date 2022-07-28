!pip install sqlalchemy_utils
!pip install uvicorn
!pip install graphene
!pip install fastapi
!pip install starlette_graphene3

from sqlalchemy import Column, String, BigInteger, Boolean, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.functions import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uvicorn
from multiprocessing import Process
import graphene
import fastapi
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
import random
import string
import requests

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

BaseModel = declarative_base()
unitedSequence = Sequence('id_seq')

# Struktury

Zamestnani_Skupiny = Table('zamestnani_skupiny', BaseModel.metadata,
                           Column('zamestnani_id', ForeignKey('zamestnani.id'), primary_key=True),
                           Column('studijniskupina_id', ForeignKey('studijniskupina.id'), primary_key=True),
                           )

Skupiny_Osoby = Table('skupiny_osoby', BaseModel.metadata,
                      Column('studijniskupina_id', ForeignKey('studijniskupina.id'), primary_key=True),
                      Column('osoba_id', ForeignKey('osoba,id'), primary_key=True),
                      )


class ZamestnaniModel(BaseModel):
    __tablename__ = 'zamestnani'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    id_skupiny = Column(BigInteger, ForeignKey('studijniskupina.id'))
    datum = Column(DateTime)

    pritomnosti = relationship('PritomnostModel', back_populates='zamestnane')
    zskupiny = relationship('UserModel', secondary=Zamestnani_Skupiny, back_populates='skupinyzamestnani')


class StudijniSkupinaModel(BaseModel):
    __tablename__ = 'studijniskupina'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    nazev = Column(String)

    skupinyzamestnani = relationship('UserModel', secondary=Zamestnani_Skupiny, back_populates='zskupiny')
    sosoby = relationship('UserModel', secondary=Skupiny_Osoby, back_populates='osobyskupiny')


class OsobaModel(BaseModel):
    __tablename__ = 'osoba'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    jmeno = Column(String)
    prijmeni = Column(String)
    id_skupina = Column(BigInteger, ForeignKey('studijniskupina.id'))
    je_Student = Column(Boolean)

    pritomnost = relationship('PritomnostModel', back_populates='osoby')
    osobyskupiny = relationship('UserModel', secondary=Skupiny_Osoby, back_populates='sosoby')


class PritomnostModel(BaseModel):
    __tablename__ = 'pritomnost'
    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    id_zamestnani = Column(BigInteger, ForeignKey('zamestnani.id'))
    id_osoby = Column(BigInteger, ForeignKey('osoba.id'))
    pritomnost = Column(String)

    zamestnane = relationship('ZamestnaniModel', back_populates='pritomnosti')
    osoby = relationship('OsobaModel', back_populates='pritomnost')


#################################################################################


engine = create_engine(connectionstring)
BaseModel.metadata.create_all(engine)

SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()

##################################################

db = SessionMaker()
userRow = ZamestnaniModel(
    id=1,
    id_skupiny=2,
    datum='2022-08-25T08:00:0.0'
)

db.add(userRow)
db.commit()
db.refresh(userRow)

##################################################

db = SessionMaker()
userRow = StudijniSkupinaModel(
    id=2,
    nazev='22-5KB1'
)

db.add(userRow)
db.commit()
db.refresh(userRow)

##################################################

db = SessionMaker()
userRow = OsobaModel(
    id=4,
    jmeno='Josef',
    prijmeni='Vomacka',
    id_skupina=2,
    je_Student=True
)

db.add(userRow)
db.commit()
db.refresh(userRow)

##################################################

db = SessionMaker()
userRow = PritomnostModel(
    id=1,
    id_zamestnani=1,
    id_osoby=4,
    pritomnost='nv'
)

db.add(userRow)
db.commit()
db.refresh(userRow)

##################################################

servers = {}
_api_process = None


def start_api(app=None, port=9992, runNew=True):
    """Stop the API if running; Start the API; Wait until API (port) is available (reachable)"""
    assert port in [9991, 9992, 9993, 9994], f'port has unexpected value {port}'

    def run():
        uvicorn.run(app, port=port, host='0.0.0.0', root_path='')

    _api_process = servers.get(port, None)
    if _api_process:
        _api_process.terminate()
        _api_process.join()
        del servers[port]

    if runNew:
        assert (not app is None), 'app is None'
        _api_process = Process(target=run, daemon=True)
        _api_process.start()
        servers[port] = _api_process


###############################################################################################################

class ZamestnaniGQL(graphene.ObjectType):
    id = graphene.ID()
    id_skupiny = graphene.ID()
    datum = graphene.DateTime()

    pritomnosti = graphene.Field(lambda: PritomnostGQL)
    zskupiny = graphene.Field(graphene.List(lambda: StudijniSkupinaGQL))


class StudijniSkupinaGQL(graphene.ObjectType):
    id = graphene.ID()
    nazev = graphene.String()

    skupinyzamestnani = graphene.Field(graphene.List(lambda: ZamestnaniGQL))
    sosoby = graphene.Field(graphene.List(lambda: OsobaGQL))


class OsobaGQL(graphene.ObjectType):
    id = graphene.ID()
    jmeno = graphene.String()
    prijmeni = graphene.String()
    id_skupina = graphene.ID()
    je_Student = graphene.Boolean()

    pritomnost = graphene.Field(lambda: PritomnostGQL)
    osobyskupiny = graphene.Field(graphene.List(lambda: StudijniSkupinaGQL))


class PritomnostGQL(graphene.ObjectType):
    id = graphene.ID()
    id_zamestnani = graphene.ID()
    id_osoby = graphene.ID()
    pritomnost = graphene.String()

    zamestnane = graphene.Field(lambda: ZamestnaniGQL)
    osoby = graphene.Field(lambda: OsobaGQL)


class QueryGQL(graphene.ObjectType):
    student = graphene.Field(OsobaGQL, id=graphene.ID(required=True))
    zamestnani = graphene.Field(ZamestnaniGQL, id=graphene.ID(required=True))
    pritomnost = graphene.Field(PritomnostGQL, id=graphene.ID(required=True))
    studijni_skupina = graphene.Field(StudijniSkupinaGQL, id=graphene.ID(required=True))

    def resolve_student(parent, info, id):
        vysledek = session.query(OsobaModel).filter(OsobaModel.id == id).first()
        return vysledek

    def resolve_zamestnani(parent, info, id):
        vysledek = session.query(ZamestnaniModel).filter(ZamestnaniModel.id == id).first()
        return vysledek

    def resolve_pritomnost(parent, info, id):
        vysledek = session.query(PritomnostModel).filter(PritomnostModel.id == id).first()
        return vysledek

    def resolve_studijni_skupina(parent, info, id):
        vysledek = session.query(StudijniSkupinaModel).filter(StudijniSkupinaModel.id == id).first()
        return vysledek

################################################################################################################xxxxxxx

import requests

def singleCache(f):
    cache = None
    def decorated():
        nonlocal cache
        if cache is None:
            fResult = f()
            cache = fResult.replace('https://swapi-graphql.netlify.app/.netlify/functions/index', '/gql')
        else:
            #print('cached')
            pass
        return cache
    return decorated

@singleCache
def getSwapi():
    source = "https://raw.githubusercontent.com/graphql/swapi-graphql/master/public/index.html"
    import requests
    r = requests.get(source)
    return r.text

graphql_app = GraphQLApp(
    schema=graphene.Schema(query=QueryGQL),
    on_get=make_graphiql_handler())

app = FastAPI()#root_path='/api')
app.add_route('/gql/', graphql_app)
start_api(app=app, port=9992, runNew=True)
def swapiUI():
    return getSwapi()

################################################################################################################xxxxxxx

start_api(app=app, port=9992, runNew=False)