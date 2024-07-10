
import os
from pathlib import Path
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import PGVector
from langchain_nomic.embeddings import NomicEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from gpt4all import gpt4all

gpt4all.DEFAULT_MODEL_DIRECTORY = Path(
    os.environ.get('NOMIC_DEFAULT_MODEL_PATH'))


class Retriever:
    def __init__(self, chunk_size, chunk_overlap, collection_name, embedding_model, inference_mode):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.inference_mode = inference_mode
        self.docs_list = self.load_documents()
        self.doc_splits = self.split_documents()
        self.vectorstore = self.create_vectorstore()

    def load_documents(self):
        docs = [WebBaseLoader(url).load() for url in self.urls]
        return [item for sublist in docs for item in sublist]

    def split_documents(self):
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        return text_splitter.split_documents(self.docs_list)

    def create_vectorstore(self):
        return PGVector.from_documents(
            documents=self.doc_splits,
            collection_name=self.collection_name,
            embedding=NomicEmbeddings(
                model=self.embedding_model, inference_mode=self.inference_mode),
            use_jsonb=True
        )

    def as_retriever(self):
        return self.vectorstore.as_retriever()


def retrieve(state):
    """
    Retrieve documents from vectorstore

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    retriever_instance = PGVector.from_existing_index(
        collection_name="rag-pgvector",
        embedding=NomicEmbeddings(
            model="nomic-embed-text-v1.5", inference_mode='local'),
        use_jsonb=True,
    )

    retriever = retriever_instance.as_retriever()
    print("---RETRIEVE---")
    question = state["question"]

    # Retrieval
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}
