import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

print("=====================================================")
print("PRODUCTION UPGRADE: LINE-BY-LINE VECTOR COMPILER")
print("=====================================================\n")

KNOWLEDGE_FILE = "knowledge.txt"
INDEX_DIR = "faiss_local_index"

if not os.path.exists(KNOWLEDGE_FILE):
    raise FileNotFoundError(f"Missing absolute data vault seed: {KNOWLEDGE_FILE}")

print(" -> Loading local sentence-transformer weights (all-MiniLM-L6-v2) offline...")
embedding_engine = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()

document_chunks = []
current_chunk = ""

print(f" -> Scanning file and parsing individual Q&A records intelligently...")
for line in lines:
    # If we encounter a new Question block, package the previous block securely
    if line.strip().startswith("Q") or line.strip().startswith("Question:"):
        if current_chunk.strip():
            doc = Document(
                page_content=current_chunk.strip(),
                metadata={"source": KNOWLEDGE_FILE, "chunk_id": len(document_chunks)}
            )
            document_chunks.append(doc)
        current_chunk = line
    else:
        current_chunk += line

# Add the absolute final chunk remaining in memory arrays
if current_chunk.strip():
    doc = Document(page_content=current_chunk.strip(), metadata={"source": KNOWLEDGE_FILE})
    document_chunks.append(doc)

print(f" -> Successfully isolated {len(document_chunks)} independent data records.")
print(f" -> Compiling high-speed FAISS vector coordinate database directory...")
vector_db = FAISS.from_documents(document_chunks, embedding_engine)

print(f" -> Freezing persistent vector index directory to: ./{INDEX_DIR}/")
vector_db.save_local(INDEX_DIR)

print("\n=====================================================")
print("SUCCESS: EVERY SINGLE QUESTION IS NOW AN INDEPENDENT VECTOR RECORD")
print("=====================================================")