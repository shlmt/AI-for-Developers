import os
from secret_key import groq_key
from langchain.chat_models import init_chat_model

if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = groq_key

llm = init_chat_model("llama3-8b-8192", model_provider="groq")

from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate

vectorstore = FAISS.load_local("faiss_index", GPT4AllEmbeddings(), allow_dangerous_deserialization=True)

cover_letter_prompt = PromptTemplate(
    input_variables=["input"],
    template="Given the company information: {input}, write a short email as cover letter by this context: {context}. just 5 sentences. If there is a relevant example or project in your resume, briefly mention it.",
)

combine_docs_chain = create_stuff_documents_chain(llm, cover_letter_prompt)
retrieval_chain = create_retrieval_chain(vectorstore.as_retriever(), combine_docs_chain)

res = retrieval_chain.invoke({"input": "BRIRI Company, Works With React & mobx & firebase"})
print(res["answer"])
