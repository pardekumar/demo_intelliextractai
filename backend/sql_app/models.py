from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    documents = relationship("Document", back_populates="owner")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    size = Column(String)
    path = Column(String)
    type = Column(String)
    vector_index = Column(String)
    status = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="documents")
    chuncks = relationship("DocumentChunck", back_populates="document")
    summary = relationship("DocumentSummary", back_populates="document")
    qna = relationship("DocumentQna", back_populates="document")


class DocumentChunck(Base):
    __tablename__ = "document_chuncks"

    id = Column(Integer, primary_key=True)
    page_content = Column(JSON)
    page_metadata = Column(JSON)
    document_id = Column(Integer, ForeignKey("documents.id"))

    document = relationship("Document", back_populates="chuncks")


class DocumentSummary(Base):
    __tablename__ = "document_summary"

    id = Column(Integer, primary_key=True)
    summary = Column(JSON)
    document_id = Column(Integer, ForeignKey("documents.id"))

    document = relationship("Document", back_populates="summary")


class DocumentQna(Base):
    __tablename__ = "document_qna"

    id = Column(Integer, primary_key=True)
    question = Column(Text)
    response = Column(JSON)
    document_id = Column(Integer, ForeignKey("documents.id"))

    document = relationship("Document", back_populates="qna")
