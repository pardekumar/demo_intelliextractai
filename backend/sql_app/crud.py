from sqlalchemy.orm import Session
from pprint import pprint
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()


def get_document_by_name(db: Session, name: str):
    return db.query(models.Document).filter(models.Document.name == name).first()


def create_user_document(db: Session, document: schemas.DocumentCreate, user_id: int):
    db_document = models.Document(**document, owner_id=user_id)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def create_document_chunck(db: Session, document_chunck: schemas.DocumentChunckCreate, document_id: int):
    try:
        db_document_chunck = models.DocumentChunck(**document_chunck, document_id=document_id)
        # print('db_document_chunck', db_document_chunck)
        # pprint(vars(db_document_chunck))
        db.add(db_document_chunck)
        db.commit()
        db.refresh(db_document_chunck)
        return db_document_chunck
    except Exception as e:
        print(db.error)
        print(str(e))


def get_document_chuncks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DocumentChunck).offset(skip).limit(limit).all()


def create_document_summary(db: Session, document_summary: schemas.DocumentSummaryCreate, document_id: int):
    try:
        db_document_summary = models.DocumentSummary(**document_summary, document_id=document_id)
        print('db_document_summary', db_document_summary)
        pprint(vars(db_document_summary))
        db.add(db_document_summary)
        db.commit()
        db.refresh(db_document_summary)
        return db_document_summary
    except Exception as e:
        print(db.error)
        print(str(e))


def create_document_qna(db: Session, document_qna: schemas.DocumentQnaCreate, document_id: int):
    try:
        db_document_qna = models.DocumentQna(**document_qna, document_id=document_id)
        print('db_document_qna', db_document_qna)
        pprint(vars(db_document_qna))
        db.add(db_document_qna)
        db.commit()
        db.refresh(db_document_qna)
        return db_document_qna
    except Exception as e:
        print(db.error)
        print(str(e))

