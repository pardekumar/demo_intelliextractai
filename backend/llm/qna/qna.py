import os
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from sql_app.main import create_qna_for_document, get_db
from sql_app.crud import get_document_by_name
from fastapi.encoders import jsonable_encoder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationalRetrievalChain
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import LLMChain
import logging
from .output_parser import get_output_parser
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_core.prompts import format_document, ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain.chains import RetrievalQA

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)
logging.getLogger("langchain.chains.llmchain").setLevel(logging.ERROR)

def generate_prompt(prompt):
    # general_system_template = r""" 
    # This is a content of literature document, please generate the answer for """+prompt.lower()+""". 
    # ----
    # {context}
    # ----
    # """
    general_system_template = r""" 
    From the given context, please help me in getting answer for """+prompt.lower()+""". 
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


def get_prompt():
    template = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Add precise values also to the answer.
Context: {summaries} 
Answer:
"""
    return template


def get_gpt_llm():
    chat_params = {
        "model": "gpt-4-1106-preview",  # Use GPT-4 model name
        "temperature": 0.5,
        "max_tokens": 4096
    }
    llm = ChatOpenAI(**chat_params)
    # llm = OpenAI(**chat_params)
    return llm


def clean_document(data):
    result = []
    for doc in data:
        result.append(doc.to_json())
    return result


DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


def get_chain(template: str, variables, verbose: bool = False):
    llm = get_gpt_llm()
    
    prompt_template = PromptTemplate(
        template=template,
        input_variables=variables,
    )
    return load_qa_with_sources_chain(
        llm=llm,
        prompt=prompt_template,
        verbose=verbose,
    )

async def data_ask(question):
    embeddings = OpenAIEmbeddings()
    llm = get_gpt_llm()
    vector_db = FAISS.load_local('emb', embeddings, allow_dangerous_deserialization=True)
    
    file_name = question.files[0]
    document = get_document_by_name(db=get_db(), name=file_name)
    if not document:
        return {"status": "error", "message": f"The document not found with name {file_name}"}
    else:
        user_question = question.prompt
        retriever = vector_db.as_retriever(search_kwargs={"k": 5, "filter": {"filename": file_name}})
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )
        res = qa_chain.invoke({"query": user_question})  # Updated to use invoke()
        return res


async def data_ask_history(question):
    # Run similarity search query
    file_name = question.files[0]
    document = get_document_by_name(db=get_db(), name=file_name)
    if (not document):
        return {"status": "error", "message": f"The document not found with name {file_name}"}
    elif document.summary:
        return jsonable_encoder(document.qna)

