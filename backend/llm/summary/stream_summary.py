from fastapi.encoders import jsonable_encoder
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from .questions import get_question
from sql_app.main import get_db
from sql_app.crud import get_document_by_name
from .summary import get_gpt_llm
import json

def serialize_document(doc):
    # If doc is a LangChain Document, convert to dict
    if hasattr(doc, 'page_content') and hasattr(doc, 'metadata'):
        return {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }
    return doc

async def stream_data_summary(params):
    embeddings = OpenAIEmbeddings()
    llm = get_gpt_llm()
    vector_db = FAISS.load_local('emb', embeddings, allow_dangerous_deserialization=True)
    file_name = params.files[0]
    document = get_document_by_name(db=get_db(), name=file_name)
    if not document:
        yield json.dumps({"status": "error", "message": f"The document not found with name {file_name}"}) + "\n"
        return
    else:
        if document.summary:
            yield json.dumps(jsonable_encoder(document.summary.__getitem__(0))["summary"]) + "\n"
            return
        else:
            questions = get_question()
            for q in questions:
                for d in q["data"]:
                    q_text = d["q"]
                    retriever = vector_db.as_retriever(search_kwargs={"k": 5, "filter": {"filename": file_name}})
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=retriever,
                        return_source_documents=True,
                    )
                    res = qa_chain.invoke({"query": q_text})
                    # Convert Document objects in res if present
                    if "source_documents" in res:
                        res["source_documents"] = [serialize_document(doc) for doc in res["source_documents"]]
                    d["res"] = res
                    yield json.dumps({"title": d["title"], "response": res}) + "\n"