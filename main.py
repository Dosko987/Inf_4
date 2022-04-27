from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

unitedSequence = Sequence('all_id_seq')

class JobModel(BaseModel):
    __tablename__ = "job"

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    id_teacher = Column(BigInteger)
    id_study_group = Column(BigInteger)
    job_name = Column(String)
    job_topic = Column(String)
    job_start = Column(DateTime)
    job_end = Column(DateTime)

class TeacherModel(BaseModel):
    __tablename__ = "teacher"

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    degree = Column(String)
    name = Column(String)
    surname = Column(String)
    department = Column(String)
    mail = Column(String)
    phone_number = Column(Integer)

class StudyGroupModel(BaseModel):
    __tablename__ = "study_group"

    faculty = Column(String)
    grade = Column(Integer)
