from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from domain.user.user_router import get_current_user
import models

router = APIRouter(
    prefix="/api/answer",
)


########
# create
########
@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(
    question_id: int, _answer_create: answer_schema.AnswerCreate,
    db: Session = Depends(get_db),
    currnet_user: models.User = Depends(get_current_user)
                    ):
    """
    `answer` 테이블 \n
    question: int
    """
    # create answer
    # question에  question_id가 존재한다면
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer_crud.create_answer(
        db, question=question, answer_create=_answer_create, user=currnet_user
                            )


@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    return answer


########
# update
########
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def anwer_update(
    _answer_update: answer_schema.AnswerUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
                ):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="데이터를 찾을 수 없습니다."
                            )
    if current_user.id != db_answer.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정 권한이 없습니다."
                            )
    answer_crud.update_answer(
        db=db, db_answer=db_answer, answer_update=_answer_update
        )


########
# delete
########
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(
    _answer_delete: answer_schema.AnswerDelete,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
                    ):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="데이터를 찾을수 없습니다."
            )
    if current_user.id != db_answer.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="삭제 권한이 없습니다."
            )
    answer_crud.delete_answer(db=db, db_answer=db_answer)


@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(_answer_vote: answer_schema.AnswerVote,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="데이터를 찾을수 없습니다."
            )
    answer_crud.vote_answer(db, db_answer=db_answer, db_user=current_user)
