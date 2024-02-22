from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle


print("Loading data...")
loader = UnstructuredFileLoader("myresume.txt")
raw_documents = loader.load()

# raw_documents = []
# for file in os.listdir('docs'):
#     if file.endswith('.pdf'):
#         pdf_path = './docs/' + file
#         loader = PyPDFLoader(pdf_path)
#         raw_documents.extend(loader.load())
#     elif file.endswith('.docx') or file.endswith('.doc'):
#         doc_path = './docs/' + file
#         loader = Docx2txtLoader(doc_path)
#         raw_documents.extend(loader.load())
#     elif file.endswith('.txt'):
#         doc_path = './docs/' + file
#         loader = TextLoader(doc_path)
#         raw_documents.extend(loader.load())

print("Splitting text...")
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=600,
    chunk_overlap=100,
    length_function=len,
)
documents = text_splitter.split_documents(raw_documents)


print("Creating vectorstore...")
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
with open("vectorstore.pkl", "wb") as f:
    pickle.dump(vectorstore, f)