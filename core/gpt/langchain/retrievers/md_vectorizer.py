
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

def load_vector_store(docs):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embeddings)
