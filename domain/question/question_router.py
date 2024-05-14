from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db #, SessionLocal
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
# from models import User # , Question
import models

from starlette import status

router = APIRouter(
    prefix="/api/question",
)

# @router.get("/list")
# def question_list():
#     # db = SessionLocal()
#     with get_db() as db:
#         _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     # db.close()
#     # 오류 여부에 상관없이 with문을 벗어나는 순간 db.close()가 실행되므로 보다 안전한 코드로 변경된 것이다.
#     return _question_list

# 비동기 방식으로 코드를 만들면 코드의 양이 많아지고 가독성도 떨어진다.
@router.get("/list", response_model=question_schema.QuestionList) #list[question_schema.Question])
def question_list(db: Session = Depends(get_db),
                    page: int = 0, size: int = 10,
                    keyword: str = ''):
    """
    `Question` 테이블 \n
    """
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size, keyword=keyword)
    return {
        'total': total,
        'question_list': _question_list
    }
    # _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    # _question_list = question_crud.get_question_list(db)
    # return _question_list

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    """
    `Question` 테이블 내용 확인 \n
    question_id: int\n
    """
    question = question_crud.get_question(db, question_id=question_id)
    return question
########
# create
########
# 리턴할 응답이 없을 경우에는 응답코드 204를 리턴하여 "응답 없음"을 나타낼 수 있다.
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create,
                                user=current_user)
########
# update
########    
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.update_question(db=db, db_question=db_question,
                                question_update=_question_update)
########
# delete
########    
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)

@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    question_crud.vote_question(db, db_question=db_question, db_user=current_user)