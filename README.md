# jump2fastapi

### 데이터베이스 Schema Design
<div class="imgContainer" align='center'>
  <img width="800" alt="dbSchemaDesign" src="https://github.com/M-05/jump2fastapi/assets/103846429/f0c45273-7075-483e-b131-d0413ad71d41">
</div>

### 디렉토리 구조
```
├── domain
│   ├── answer
│   │   ├── answer_crud.py
│   │   ├── answer_router.py
│   │   └── answer_schema.py
│   ├── question
│   │   ├── question_crud.py
│   │   ├── question_router.py
│   │   └── question_schema.py
│   └── user
│       ├── user_crud.py
│       ├── user_router.py
│       └── user_schema.py
├── database.py
├── main.py
└── models.py
```
### FastAPI Docs
<div class="docsContainer" align='center'>
  <img width="390" alt="FastAPI Docs1" src="https://github.com/M-05/jump2fastapi/assets/103846429/502dba35-8e47-4df1-8691-4f30ebb98679">
  <img width="380" alt="FastAPI Docs2" src="https://github.com/M-05/jump2fastapi/assets/103846429/40e9f18c-bbd5-4103-b19a-ad799e4f5c5b">
</div>

### 모델 속성
  
<div class="tableContainer" align='center'>
  
|`Question`|속성명|설명|`Answer`|속성명|설명|`User`|속성명|설명|
|--|--|--|--|--|--|--|--|--|
||id|질문 데이터의 고유 번호||id|답변 데이터의 고유 번호||id|사용자 고유 번호|
||subject|질문 제목||content|답변 내용||username|사용자 이름|
||content|질문 내용||create_date|답변 작성일시||password|비밀번호|
||create_date|질문 작성일시||create_date|답변 작성일시||email|이메일|
||user_id|질문 작성자의 고유 번호||user_id|답변 작성자의 고유 번호||||
||user|질문 작성자||user|답변 작성자||||
||modify_date|질문 수정일시||modify_date|답변 수정일시||||
||vote|질문 추천||vote|답변 추천||||

</div>

### API 명세

<div class="apiContainer" align='center'>
  
|`Question`|API명|URL|요청방법|설명|
|--|--|--|--|--|
| |질문 상세조회|/api/question/detail/detail/{question_id}|get|질문 상세 내역 조회|
| |질문 등록|/api/question/create|post|질문 등록|
| |질문 수정|/api/question/update|put|질문 수정|
| |질문 삭제|/api/question/delete|delete|질문 삭제|
| |질문 추천|/api/question/vote|post|질문 추천|

|`Answer`|API명|URL|요청방법|설명|
|--|--|--|--|--|
| |답변 상세조회|/api/answer/detail/detail/{question_id}|get|답변 상세 내역 조회|
| |답변 등록|/api/answer/create|post|질문에 대한 답변 등록|
| |답변 수정|/api/answer/update|put|답변 수정|
| |답변 삭제|/api/answer/delete|delete|답변 삭제|
| |답변 추천|/api/answer/vote|post|답변 추천|

|`User`|API명|URL|요청방법|설명|
|--|--|--|--|--|
| |회원 가입|/api/user/create|post|회원 등록|
| |로그인|/api/user/login|post|로그인|

</div>

> 로그인 API 출력 항목
- access_token : 접근 토큰
- token_type : 토큰 종류(Bearer로 고정하여 사용. Bearer는 JWT 또는 OAuth의 토큰방식)
- username : 사용자명



