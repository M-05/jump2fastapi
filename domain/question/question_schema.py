import datetime
from pydantic import BaseModel, field_validator
# BaseModel. 입력데이터를 보장해주는게 아니라 입력을 받아 데이터 형식과 제약조건을 보장해주는 모델이다.
from domain.answer import answer_schema
from domain.user import user_schema


class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[answer_schema.Answer] = []
    user: user_schema.User | None
    modify_date: datetime.datetime | None = None
    voter: list[user_schema.User] = []

    class Config:
        orm_mode = True
    #  Question 모델의 항목들이 자동으로 Question 스키마로 매핑된다.


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []


###################################
# Update(QuestionCreate(BaseModel))
###################################
class QuestionUpdate(QuestionCreate):
    question_id: int


class QuestionDelete(BaseModel):
    question_id: int


class QuestionVote(BaseModel):
    question_id: int
