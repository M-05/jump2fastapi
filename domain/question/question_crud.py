from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
import models

from sqlalchemy import and_
from sqlalchemy.orm import Session


# def get_question_list(db: Session):
#     question_list = db.query(Question)\
#         .order_by(Question.create_date.desc())\
#         .all()
#     return question_list
def get_question_list(db: Session, skip: int = 0, limit: int = 10, 
                    keyword: str = ''):
    question_list = db.query(models.Question)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(models.Answer.question_id, models.Answer.content, models.User.username) \
            .outerjoin(models.User, and_(models.Answer.user_id == models.User.id)).subquery()
        question_list = question_list \
            .outerjoin(models.User) \
            .outerjoin(sub_query, and_(sub_query.c.question_id == models.Question.id)) \
            .filter(models.Question.subject.ilike(search) |        # 질문제목
                    models.Question.content.ilike(search) |        # 질문내용
                    models.User.username.ilike(search) |           # 질문작성자
                    sub_query.c.content.ilike(search) |     # 답변내용
                    sub_query.c.username.ilike(search)      # 답변작성자
                    )
    total = question_list.distinct().count()
    question_list = question_list.order_by(models.Question.create_date.desc())\
        .offset(skip).limit(limit).distinct().all()
    _question_list = db.query(models.Question)\
        .order_by(models.Question.create_date.desc())

    total = _question_list.count()
    question_list = _question_list.offset(skip).limit(limit).all()
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_question(db: Session, question_id: int):
    question = db.query(models.Question).get(question_id)
    return question

def create_question(db: Session, question_create: QuestionCreate,
                    user : models.User):
    db_question = models.Question(subject=question_create.subject,
                            content=question_create.content,
                            create_date=datetime.now(),
                            user=user)
    db.add(db_question)
    db.commit()

def update_question(db: Session, db_question: models.Question,
                    question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()

def delete_question(db: Session, db_question: models.Question):
    db.delete(db_question)
    db.commit()

def vote_question(db: Session, db_question: models.Question, db_user: models.User):
    db_question.voter.append(db_user)
    db.commit()