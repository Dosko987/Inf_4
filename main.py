from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import database_exists, create_database

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
