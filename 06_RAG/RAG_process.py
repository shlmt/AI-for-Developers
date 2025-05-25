from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS

loader = PyPDFLoader(file_path="./cv.pdf")
document = loader.load()

splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
split_doc = splitter.split_documents(document)

embeddings = GPT4AllEmbeddings()

vectorstore = FAISS.from_documents(split_doc, embeddings)
vectorstore.save_local("faiss_index")
