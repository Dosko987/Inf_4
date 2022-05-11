from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
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

class JobModel(BaseModel):
    __tablename__ = "job"

    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    id_teacher = Column(BigInteger)
    id_study_group = Column(BigInteger)
    job_name = Column(String)
    job_topic = Column(String)
    job_start = Column(DateTime)
    job_end = Column(DateTime)


class TeacherModel(BaseModel):
    __tablename__ = "teacher"

    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    degree = Column(String)
    name = Column(String)
    surname = Column(String)
    department = Column(String)
    mail = Column(String)
    phone_number = Column(Integer)


class StudyGroupModel(BaseModel):
    __tablename__ = "study_group"

    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    faculty = Column(String)
    grade = Column(Integer)
    group_name = Column(String)


class StudentsModel(BaseModel):
    __tablename__ = "students"

    id = Column(BigInteger, Sequence('id_seq'), primary_key=True)
    group_name = Column(String)
    absent_students = Column(BigInteger)
    present_students = Column(BigInteger)


class AbsentStudentsModel(BaseModel):
    __tablename__ = "absent"

    absent_students = Column(BigInteger)
    rank = Column(String)
    name = Column(String)
    surname = Column(String)
    reason = Column(String)


class PresentStudentsModel(BaseModel):
    __tablename__ = "present"

    present_students = Column(BigInteger)
    rank = Column(String)
    name = Column(String)
    surname = Column(String)


#################################################################################

# Inicializase struktur
BaseModel.metadata.create_all(engine)

# Session

SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()
session.close()


# Naplneni database
def get_random_string(length):
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(length))
    return result


def randomUser(i):
    surNames = [
        'Novák', 'Nováková', 'Svobodová', 'Svoboda', 'Novotná',
        'Novotný', 'Dvořáková', 'Dvořák', 'Černá', 'Černý',
        'Procházková', 'Procházka', 'Kučerová', 'Kučera', 'Veselá',
        'Veselý', 'Horáková', 'Krejčí', 'Horák', 'Němcová',
        'Marková', 'Němec', 'Pokorná', 'Pospíšilová', 'Marek'
    ]

    names = [
        'Jiří', 'Jan', 'Petr', 'Jana', 'Marie', 'Josef',
        'Pavel', 'Martin', 'Tomáš', 'Jaroslav', 'Eva',
        'Miroslav', 'Hana', 'Anna', 'Zdeněk', 'Václav',
        'Michal', 'František', 'Lenka', 'Kateřina',
        'Lucie', 'Jakub', 'Milan', 'Věra', 'Alena'
    ]

    ranks = [
        'svob', 'des', 'čet', 'rtn', 'rtm'
    ]

    degree1 = [
        'Ing.', 'Mgr.', 'RNDr.', 'Dr.'
    ]

    department1 = [
        'K201', 'K202', 'K203', 'K204', 'K205', 'K206', 'K207', 'K208', 'K209'
    ]

    number = [
        '123456789', '987654321', '456789123', '321644598', '987456123', '123365489', '156891238'
    ]

    degree = random.choice(degree1)
    rank = random.choice(ranks)
    name1 = random.choice(names)
    name2 = random.choice(surNames)
    phone = random.choice(number)
    department = random.choice(department1)

    if (i == 1):
        return {'rank': f'{rank}', 'name': f'{name1}', 'surname': f'{name2}', 'email': f'{name1}.{name2}@unob.cz'}
    else:
        return {'degree': f'{degree}', 'name': f'{name1}', 'surname': f'{name2}', 'email': f'{name1}.{name2}@unob.cz',
                'phone_number': f'{phone}', 'department': f'{department}'}


def PopulateStudents(count=10, group=None):
    for i in range(count):
        userNames = randomUser(1)
        crudUserCreate(db=session, user=StudentsModel(**userNames))


def PopulateTeachers(count=4, group=None):
    for i in range(count):
        userNames = randomUser(2)
        crudUserCreate(db=session, user=StudentsModel(**userNames))


session = SessionMaker()
PopulateUsers(10)
session.close()
