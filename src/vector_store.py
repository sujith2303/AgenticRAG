from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import os
from config import Config

from abc import ABC, abstractmethod

os.environ["GOOGLE_API_KEY"] = Config.GEMINI_API_KEY
class DocumentLoader(ABC):
    ## Created an abstract interface for the document loader. This follows principle of strategy design pattern. This allows us to create different strategies for loading documents.
    ## We can add webbased loader in future 
    @abstractmethod 
    def load(self):
        pass
    @abstractmethod
    def retrieve(self, query: str):
        pass 
    
class LocalFileLoader(DocumentLoader):
    def __init__(
                self, 
                 embeddings_model="models/embedding-001", 
                 collection_name="example_collection", 
                 persist_directory="./chroma_langchain_db",
                 chunk_size = 1000,
                 chunk_overlap = 200,
                 start_index = True
                 ):
        embeddings = GoogleGenerativeAIEmbeddings(model=embeddings_model)
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=persist_directory,
        )
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.start_index = start_index

    def load(self, path):
        file_extension = os.path.splitext(path)[1].lower()

        if file_extension == ".pdf":
            loader = PyPDFLoader(path)
        elif file_extension == ".docx":
            loader = Docx2txtLoader(path)
        elif file_extension == ".txt":
            loader = TextLoader(path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        docs = loader.load()
        all_splits = self.split_document(docs)
        self.vector_store.add_documents(documents=all_splits)

    def retrieve(self, query: str):
        return self.vector_store.similarity_search(query, k=3)

    def split_document(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            add_start_index=self.start_index,
        )
        all_splits = text_splitter.split_documents(docs)
        return all_splits


