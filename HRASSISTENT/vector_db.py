from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

#FAISS Facebook AI Similarity Search is a library for efficient similarity search and clustering of dense vectors.
#IT is used to create a vector database that allows for fast retrieval of similar items based on their vector representations.

root = Path(".")
#create vector database from the existing .txt files in the current directory.
#This will allow us to perform similarity search and retrieval based on the content of these documents.
text_files = sorted(root.glob("*.txt"))
if not text_files:
    raise FileNotFoundError("No .txt documents were found in the workspace root to index.")

# Load documents from the existing policy / JD files in the workspace.
documents = []
for file_path in text_files:
    loader = TextLoader(str(file_path), encoding="utf-8")
    documents.extend(loader.load())

print(f"Loaded {len(documents) } documents")

# Split documents into searchable chunks.
# Documents are splitted into chunks of 500 characters with an overlap of 50 characters 
# to ensure that the context is preserved across chunks and to improve the quality of search results.
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# Create embeddings and persist the FAISS vector store.
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_db = FAISS.from_documents(chunks, embeddings)
#This code creates a FAISS vector store from the document chunks using the specified embeddings model.
#It works by converting each document chunk into a vector representation using the OllamaEmbeddings 
#model and then storing these vectors in the FAISS index for efficient similarity search and retrieval.
output_dir = Path("hr_vector_db")
output_dir.mkdir(exist_ok=True)
vector_db.save_local(str(output_dir))
print(f"Vector Database Created at {output_dir.resolve()}")