from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        print('gggggggggg')
        # db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=get_db(), email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=get_db(), user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=get_db(), skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=get_db(), user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/documents/", response_model=schemas.Document)
def create_document_for_user(
    user_id: int, document: schemas.DocumentCreate, db: Session = Depends(get_db)
):
    return crud.create_user_document(db=get_db(), document=document, user_id=user_id)


@app.get("/document/chuncks", response_model=list[schemas.Document])
def read_document_chuncks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chuncks = crud.get_document_chuncks(db=get_db(), skip=skip, limit=limit)
    return chuncks


@app.post("/documents/{document_id}/chuncks/", response_model=schemas.DocumentChunck)
def create_chunck_for_document(
    document_id: int, document_chunck: schemas.DocumentChunckCreate, db: Session = Depends(get_db)
):
    return crud.create_document_chunck(db=get_db(), document_chunck=document_chunck, document_id=document_id)


@app.post("/documents/{document_id}/summary/", response_model=schemas.DocumentSummary)
def create_summary_for_document(
    document_id: int, document_summary: schemas.DocumentSummaryCreate, db: Session = Depends(get_db)
):
    return crud.create_document_summary(db=get_db(), document_summary=document_summary, document_id=document_id)


@app.post("/documents/{document_id}/qna/", response_model=schemas.DocumentQna)
def create_qna_for_document(
    document_id: int, document_qna: schemas.DocumentQnaCreate, db: Session = Depends(get_db)
):
    return crud.create_document_qna(db=get_db(), document_qna=document_qna, document_id=document_id)
