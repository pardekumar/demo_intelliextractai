import os, json
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
# from langchain_community.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from .questions import get_question
from sql_app.main import create_summary_for_document, get_db
from sql_app.crud import get_document_by_name
from fastapi.encoders import jsonable_encoder

def generate_prompt(prompt):
    general_system_template = r""" 
    Given a specific context, please transform the answer into """+prompt.lower()+""" manner. 
     ----
    {context}
    ----
    """

    print("Prompt is = {}".format(general_system_template))
    general_user_template = "Question:```{question}```"
    messages = [
        SystemMessagePromptTemplate.from_template(general_system_template),
        HumanMessagePromptTemplate.from_template(general_user_template)
    ]
    qa_prompt = ChatPromptTemplate.from_messages( messages )
    return qa_prompt


def get_gpt_llm():
    chat_params = {
        "model": "gpt-3.5-turbo-16k", # Bigger context window
        "temperature": 0.5, # To avoid pure copy-pasting from docs lookup
        "max_tokens": 8000
    }
    llm = ChatOpenAI(**chat_params)
    return llm


def clean_document(res):
    result = []
    for doc in res["input_documents"]:
        result.append(doc.to_json())
    res["input_documents"] = result
    return res


async def data_summary(question):
    embeddings = OpenAIEmbeddings()
    llm = get_gpt_llm()
    vector_db = Chroma(persist_directory='emb', embedding_function=embeddings)

    # Run similarity search query
    file_name = question.files[0]
    document = get_document_by_name(db=get_db(), name=file_name)
    if (not document):
        return {"status": "error", "message": f"The document not found with name {file_name}"}
    else:
        # try:
        if document.summary:
            return jsonable_encoder(document.summary.__getitem__(0))["summary"]
            # return document.summary.__getitem__(0).__getstate__()["summary"]
        else:
            questions = get_question()
            for q in questions:
                for d in q["data"]:
                    print(d["q"])
                    q = d["q"]
                    v = vector_db.similarity_search(query=q, filter={ "filename": file_name })
                    # v = vector_db.similarity_search(query=q)
                    # print('---------------------', v)
                    # d["res"] = v

                    chain = load_qa_chain(llm, chain_type="stuff")

                    res = clean_document(chain({ "input_documents": v, "question": q }))
                    d["res"] = res
            create_summary_for_document(document_id=document.id, document_summary={
                "summary": questions,
            })
            return questions
        # except Exception:
        #     return "There was an error getting summary, please try again"

    # res = v
    # return res