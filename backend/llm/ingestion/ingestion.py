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


def page_hashing(page):
    hash_object = hashlib.md5()
    hash_object.update(page.encode())
    return hash_object.hexdigest()


def remove_duplicates(hash_dict, hash_page_dict, pages, file, filename):
    for page in pages:
        page_hash = page_hashing(page.page_content)
        if page_hash not in hash_dict.values():
            hash_dict[page_hash] = page_hash
            hash_page_dict[page_hash] = {"page": page, "file": file, "filename": filename}
    return hash_dict


def getValidIndexName(data):
    data = data.lower()
    chars = re.escape(string.punctuation)
    return re.sub('['+chars+']', '', data)


async def data_ingestion(pdf_files, filenames, document_id=None):
    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=160
    )
    hash_dict = {}
    hash_page_dict = {}
    print("pdf_files", pdf_files)
    for index, file in enumerate(pdf_files):
        print("index", index)
        print("file", file)
        loader = PyPDFLoader(file)
        print("loader", loader, loader.load())
        # pages = loader.load_and_split()
        pages = text_splitter.split_documents(loader.load())
        print("pages", pages)
        filename = filenames[index]
        remove_duplicates(hash_dict, hash_page_dict, pages, file, filename)
        # remove_duplicates(hash_dict, hash_page_dict, pages, file, filename)
        # print(pages, len(pages), hash_dict, len(hash_dict))

    final_docs = []
    final_meta = []
    cnt = 0
    for hash_val in hash_dict.keys():
        cnt = cnt + 1
        docs = hash_page_dict[hash_val]["page"]
        file = hash_page_dict[hash_val]["file"]
        filename = hash_page_dict[hash_val]["filename"]
        # docs.metadata.update({**docs.metadata, "filename": filename})
        docs.metadata["filename"] = filename
        # return docs
        # print('1111111111111111111111111111', docs)
        # chunck = create_chunck_for_document(document_id=document_id, document_chunck={
        #     "page_content": { "page_content": docs.page_content },
        #     "page_metadata": docs.metadata,
        # })

        final_docs.append(docs)
        final_meta.append(file)

    db = FAISS.from_documents(
        documents=final_docs,
        embedding=embeddings,
        # metadatas=[{"source": f"{final_meta[i]}"} for i in range(len(final_meta))],
    )
    db.save_local("emb")
    return final_docs
    # db.persist()
