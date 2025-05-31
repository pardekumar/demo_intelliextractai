import os, json
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from .questions import get_question
from sql_app.main import create_summary_for_document, get_db
from sql_app.crud import get_document_by_name
from fastapi.encoders import jsonable_encoder
from langchain.chains import RetrievalQA  # <-- Add this import

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
        "model": "gpt-4-1106-preview",  # Updated to GPT-4 model
        "temperature": 0.5, # To avoid pure copy-pasting from docs lookup
        "max_tokens": 4096
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
    vector_db = FAISS.load_local('emb', embeddings, allow_dangerous_deserialization=True)

    # Run similarity search query
    file_name = question.files[0]
    document = get_document_by_name(db=get_db(), name=file_name)
    if (not document):
        return {"status": "error", "message": f"The document not found with name {file_name}"}
    else:
        if document.summary:
            return jsonable_encoder(document.summary.__getitem__(0))["summary"]
        else:
            questions = get_question()
            for q in questions:
                for d in q["data"]:
                    print(d["q"])
                    q_text = d["q"]
                    v = vector_db.similarity_search(query=q_text, filter={ "filename": file_name })

                    # Use RetrievalQA instead of load_qa_chain
                    retriever = vector_db.as_retriever(search_kwargs={"k": 5, "filter": {"filename": file_name}})
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=retriever,
                        return_source_documents=True,
                    )
                    res = qa_chain.invoke({"query": q_text})
                    d["res"] = res
                    print("data_summary", res)
            # create_summary_for_document(document_id=document.id, document_summary={
            #     "summary": questions,
            # })
            return questions