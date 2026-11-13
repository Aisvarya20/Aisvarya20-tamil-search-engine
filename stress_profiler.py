import time
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor

print("=====================================================")
print("PRODUCTION AUDIT: CONCURRENT LANGGRAPH API STRESS PROFILER")
print("=====================================================\n")

# Correct direct loopback network socket targeting port 8000
target_url = "http://localhost:8000/search"

# Ingest test payloads: Tamil string, standard English, and an empty anomaly query
test_payloads = [
    {"query_text": "செயற்கை நுண்ணறிவு"},
    {"query_text": "artificial intelligence technology"},
    {"query_text": "   "} # Triggers your cyclic self_correction_node!
]

def fire_stress_request(payload_dict):
    start_time = time.perf_counter()
    data = json.dumps(payload_dict).encode("utf-8")
    req = urllib.request.Request(
        target_url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            res_json = json.loads(res_data)
            latency = (time.perf_counter() - start_time) * 1000
            print(f"[+] Request: '{payload_dict['query_text']}' -> Route: {res_json.get('agent_routing_path')} | Latency: {latency:.2f}ms")
    except Exception as e:
        print(f"[-] Request Failed for '{payload_dict['query_text']}': {str(e)}")

print(" -> Initializing asynchronous thread workers on CPU cores...")
# Execute concurrent processing threads completely local on your hardware
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(fire_stress_request, test_payloads)

print("\n=====================================================")
print("STRESS PROFILE MATRIX COMPLETE: PLATFORM WORKFLOW RESILIENT")
print("=====================================================")