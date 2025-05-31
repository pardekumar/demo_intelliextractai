import os
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_community.vectorstores import Chroma
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re, string, hashlib
from sql_app.main import create_chunck_for_document
import re
import base64
import chromadb
from chromadb.config import Settings


client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="emb"))



async def get_all_data(pdf_files, filenames, document_id):
    db = Chroma.from_documents(
        documents=final_docs,
        embedding=embeddings,
        # metadatas=[{"source": f"{final_meta[i]}"} for i in range(len(final_meta))],
        persist_directory='emb'
    )
    return final_docs
    # db.persist()
