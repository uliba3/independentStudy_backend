import requests

#response = requests.get("http://localhost:8000/search", params={"query": "I want to learn about Africa"})
response = requests.get("http://localhost:8000/ask", params={"query": "What does it say?", "id": 1})

try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Could not decode JSON response")
