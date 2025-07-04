import requests

url = "http://127.0.0.1:8000/analyze"
file_path = "data/sample.pdf"  # change if your test file is different

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Response:")
print(response.text)
