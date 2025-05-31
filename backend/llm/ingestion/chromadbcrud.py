import os
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_community.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re, string, hashlib
from sql_app.main import create_chunck_for_document
import re
import base64


async def get_all_data(pdf_files, filenames, document_id):
    db = FAISS.from_documents(
        documents=final_docs,
        embedding=embeddings,
        # metadatas=[{"source": f"{final_meta[i]}"} for i in range(len(final_meta))],
    )
    # db.save_local('emb')  # Uncomment if you want to persist the FAISS index
    return final_docs
    # db.persist()
