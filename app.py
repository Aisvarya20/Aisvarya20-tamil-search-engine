import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from graph_agent import compiled_graph_agent
# Import our automated audit logger engine directly from our local module asset
from agent_logger import append_audit_log

print("=====================================================")
print("PRODUCTION LAUNCH: STATEFUL LANGGRAPH INTEGRATION SERVER")
print("=====================================================\n")

class LangGraphAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Exposes a secure system environment runtime health route."""
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            health_status = {"status": "healthy", "database_vault_bound": True}
            self.wfile.write(json.dumps(health_status).encode("utf-8"))
            
    def do_POST(self):
        """Intercepts unstructured text streams, pipes through LangGraph, and automates audits."""
        if self.path == "/search":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode("utf-8"))
            
            user_query = payload.get("query_text", "")
            print(f"\n[API Gateway Ingestion] Intercepted incoming payload query: '{user_query}'")
            
            try:
                # Invoke the compiled multi-agent state graph loop completely offline
                graph_state_output = compiled_graph_agent.invoke(
                    {"current_query": user_query, "error_flag": False}
                )
                
                results_list = graph_state_output.get("search_results", [])
                routing_track = graph_state_output.get("routing_decision", "completed")
                
                # AUTOMATED AUDIT TRAIL: Trigger persistent log updates dynamically to disk
                append_audit_log(user_query, routing_track, len(results_list))
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                
                response_payload = {
                    "input_query": user_query,
                    "agent_routing_path": routing_track,
                    "extracted_matches": results_list
                }
                self.wfile.write(json.dumps(response_payload).encode("utf-8"))
                print("[API Gateway Routing] Successfully dispatched processed graph memory arrays.")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

if __name__ == "__main__":
    print(" -> Starting absolute direct HTTP network listener on port 8000...")
    server = HTTPServer(("127.0.0.1", 8000), LangGraphAPIHandler)
    print(" -> Server online: http://127.0.0.1:8000")
    server.serve_forever()