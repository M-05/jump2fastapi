# FastAPI 프로젝트의 전체적인 환경을 설정하는 파일
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router

# import models
# from database import engine
# models.Base.metadata.create_all(bind=engine)
# 테이블이 존재하지 않을 경우에만 테이블을 생성한다. 한번 생성된 테이블에 대한 변경 관리를 할 수는 없다

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router, tags=["question"])
app.include_router(answer_router.router, tags=["answer"])
app.include_router(user_router.router, tags=["users"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=5173, reload=True)