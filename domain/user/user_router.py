from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
# jwt란 Json 포맷을 이용하여 사용자에 대한 속성을 저장하는 Claim 기반의 Web Token이다.

from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
# import secrets
# secrets.token_hex(32)
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c"
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES - 토큰의 유효기간을 의미한다. 분 단위로 설정한다.
# SECRET_KEY - 암호화시 사용하는 64자리의 랜덤한 문자열이다.
# ALGORITHM - 토큰 생성시 사용하는 알고리즘을 의미하며 여기서는 HS256을 사용한다.
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user"
)
########
# create
########
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    `signup`\n
    username: str\n
    password: str\n
    email: EmailStr\n
    """
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)
########
# login
########
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                            db: Session = Depends(get_db)):
    """
    `login` with `user_schema.Token` \n 
    grant_type : optional[...] = None\n
    username : str\n
    password : str\n
    scope : optional[str] = None\n
    client_id : optional[...] = None
    client_secret : optional[...] = None
    """
    #########################
    # Check user and password
    #########################
    user = user_crud.get_user(db, form_data.username)
    if not user or not user_crud.pwd_context.verify(form_data.password, user.password):
    # user_crud.CryptContext(schemes=["bcrypt"], deprecated="auto")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="올바르지 않는 사용자 or 비밀번호 입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #########################
    # make access token
    #########################
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username

    }

def get_current_user(token: str = Depends(oauth2_schema), # OAuth2PasswordBearer(tokenUrl="/api/user/login")
                    db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # user.username

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # 사용자명이 없거나 해당 사용자명으로 사용자 데이터 조회에 실패할 경우에는 credentials_exception 예외를 발생
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user