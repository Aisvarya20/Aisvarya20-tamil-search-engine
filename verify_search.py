import os
import sys
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def run_offline_vault_diagnostics():
    print("=====================================================")
    print("RUNNING SATURDAY LOCAL FAISS DATABASE STORAGE AUDITS")
    print("=====================================================\n")
    
    db_storage_name = "faiss_local_index"
    
    # Validation Check: Confirm physical binary structures exist on disk
    if not os.path.exists(db_storage_name):
        print(f"[-] Diagnostic Failure: Folder '{db_storage_name}' missing on local disk storage.")
        sys.exit(1)
        
    print(" -> Loading local sentence-transformer weights offline...")
    embedding_engine = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print(f" -> Mapping spatial binary index arrays out of: ./{db_storage_name}")
    local_vault = FAISS.load_local(
        db_storage_name, 
        embedding_engine, 
        allow_dangerous_deserialization=True
    )
    
    # Test Payload Definition: Run semantic matching for a Tamil concept phrase
    test_query = "செயற்கை நுண்ணறிவு தொழில்நுட்பம்"
    print(f"\n[Test Query Trigger] Executing vector similarity search for: '{test_query}'")
    
    # Calculate geometric similarity search paths completely offline
    matched_results = local_vault.similarity_search(test_query, k=1)
    
    print("\n=====================================================")
    print("DIAGNOSTIC RETRIEVAL RESULTS SPARKED SUCCESSFULLY:")
    print("=====================================================")
    for idx, doc in enumerate(matched_results, start=1):
        print(f"\n[Rank #{idx}] Matched Text Content:")
        print(f"-> {doc.page_content}")
        print(f"\nAssociated Metadata Map: {doc.metadata}")
    print("\n=====================================================")

if __name__ == "__main__":
    run_offline_vault_diagnostics()