import re
from typing import Dict, List, Any
from langgraph.graph import StateGraph, END
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("=====================================================")
print("PRODUCTION REBOOT: OFFLINE VECTOR SEARCH ENGINE")
print("=====================================================\n")

class AgentState(dict):
    current_query: str
    search_results: List[str]
    routing_decision: str
    error_flag: bool

INDEX_DIR = "faiss_local_index"

# Initialize local semantic embedding and FAISS vector database directory layers
print(" -> Loading local semantic index configurations from disk...")
embedding_engine = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = FAISS.load_local(INDEX_DIR, embedding_engine, allow_dangerous_deserialization=True)

REGEX_MASK = re.compile(r'[\u0B80-\u0BFF\u0020-\u007E]+')

def linguistic_sanitization_node(state: Dict[str, Any]) -> Dict[str, Any]:
    query = state.get("current_query", "").strip()
    sanitized = "".join(REGEX_MASK.findall(query))
    if not sanitized:
        return {"current_query": "ERROR_EMPTY_INPUT", "error_flag": True}
    return {"current_query": sanitized, "error_flag": False}

def self_correction_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print(" -> [LangGraph Interceptor] Malformed query caught! Injecting recovery path...")
    return {"current_query": "Aisha project details", "error_flag": False}

def vector_vault_node(state: Dict[str, Any]) -> Dict[str, Any]:
    user_query = state.get("current_query")
    print(f" -> [Database Node] Scanning index maps for: '{user_query}'")
    
    # Run absolute semantic search vector match against your 200 compiled questions
    matched_docs = vector_db.similarity_search(user_query, k=1)
    results = [doc.page_content for doc in matched_docs] if matched_docs else ["No matching records found."]
    
    return {"search_results": results, "routing_decision": "vector_vault_node"}

def conditional_routing_edge(state: Dict[str, Any]) -> str:
    if state.get("error_flag") is True:
        return "trigger_recovery"
    return "trigger_search"

builder = StateGraph(AgentState)
builder.add_node("linguistic_sanitization_node", linguistic_sanitization_node)
builder.add_node("self_correction_node", self_correction_node)
builder.add_node("vector_vault_node", vector_vault_node)

builder.set_entry_point("linguistic_sanitization_node")
builder.add_conditional_edges(
    "linguistic_sanitization_node",
    conditional_routing_edge,
    {
        "trigger_recovery": "self_correction_node",
        "trigger_search": "vector_vault_node"
    }
)
builder.add_edge("self_correction_node", "vector_vault_node")
builder.add_edge("vector_vault_node", END)

compiled_graph_agent = builder.compile()
print("Stateful Multi-Agent Graph compiled successfully.")