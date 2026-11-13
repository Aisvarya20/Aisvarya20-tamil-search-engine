import json
import urllib.request

print("=====================================================")
print("LAUNCHING LIVE CORE SEARCH API VALIDATION LOGS")
print("=====================================================\n")

# Correct direct loopback network socket targeting port 8000
target_url = "http://localhost:8000/search"

# Test Payload: Standard Tamil search string array mapping
payload_data = {"query_text": "செயற்கை நுண்ணறிவு"}

encoded_bytes = json.dumps(payload_data).encode("utf-8")

request_packet = urllib.request.Request(
    target_url,
    data=encoded_bytes,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    print(f" -> Injecting query packet into backend gateway: '{payload_data['query_text']}'")
    with urllib.request.urlopen(request_packet) as network_channel:
        response_raw = network_channel.read().decode("utf-8")
        response_json = json.loads(response_raw)
        
        print("\n[+] CONNECTION SUCCESS: 200 OK EXTRACTED")
        print(f"[+] Agent Routing Pathway Selected: {response_json.get('agent_routing_path')}")
        print("\n=====================================================")
        print("SEMANTIC MATCHES RETRIEVED FROM LOCAL FAISS VAULT:")
        print("=====================================================")
        for index, match in enumerate(response_json.get("extracted_matches", []), start=1):
            print(f" Chunk Match #{index}:")
            print(f"  -> Extracted Text Content: {match.get('content')}")
            print(f"  -> Factual Source Document: {match.get('metadata', {}).get('source')}")
        print("=====================================================")
except Exception as network_error:
    print(f"\n[-] Critical Connection Blocked: {str(network_error)}")