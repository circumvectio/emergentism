import urllib.request
import json

base_url = "https://api.osf.io/v2/nodes/xk3yc/files/"
req = urllib.request.Request(base_url)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
