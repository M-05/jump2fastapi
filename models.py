# ORM(object relational mapping)을 지원하는 파이썬 데이터베이스 도구인 SQLAlchemy를 사용한다. SQLAlchemy는 모델 기반으로 데이터베이스를 처리한다.
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base

question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)
# ManyToMany 관계를 적용하기 위해서는 sqlalchemy의 Table을 사용하여 N:N 관계를 의미하는 테이블을 먼저 생성해야 한다.
answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False) # 고정 길이 문자열
    content = Column(Text, nullable=False)   # 가변 길이 문자열
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=question_voter, backref='question_voters')

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    # question_id 속성은 답변을 질문과 연결하기 위해 추가한 속성이다. 
    # 답변은 어떤 질문에 대한 답변인지 알아야 하므로 질문의 id 속성이 필요하다
    question = relationship("Question", backref="answers")
    #  첫 번째 파라미터는 참조할 모델명이고 두 번째 backref 파라미터는 역참조 설정
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=answer_voter, backref='answer_voters')


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

