from passlib.context import CryptContext
# 비밀번호는 탈취되더라도 복호화 할 수 없는 값으로 암호화 해서 저장해야 한다.
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# bcrypt 알고리즘을 사용하는 pwd_context 객체를 생성하고 pwd_context 객체를 사용하여 비밀번호를 암호화하여 저장했다.

def create_user(db: Session, user_create: UserCreate):
    db_user = models.User(username=user_create.username,
                    password=pwd_context.hash(user_create.password1),
                    email=user_create.email)
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(models.User).filter(
        (models.User.username == user_create.username) |
        (models.User.email == user_create.email)
    ).first()

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()