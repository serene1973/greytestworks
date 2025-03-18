import requests

url = "https://jsonplaceholder.typicode.com/posts/1"  # Example API
response = requests.get(url)

print(response.status_code)  # Check HTTP status
print(response.json())  # Print response body



headers = {
    "Authorization": "Bearer your_token_here",
    "Content-Type": "application/json"
}

params = {
    "userId": 1
}

response = requests.get("https://jsonplaceholder.typicode.com/posts", headers=headers, params=params)
print(response.json())




url = "https://jsonplaceholder.typicode.com/posts"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_token_here"
}

body = {
    "title": "Automated API Test",
    "body": "This is a test API request",
    "userId": 1
}

response = requests.post(url, headers=headers, json=body)
print(response.status_code)
print(response.json())  # API response



response = requests.put(url + "/1", headers=headers, json={"title": "Updated Title"})
print(response.json())


response = requests.delete(url + "/1", headers=headers)
print(response.status_code)  # 200 means success



session = requests.Session()
session.headers.update({"Authorization": "Bearer your_token_here"})

response = session.get("https://jsonplaceholder.typicode.com/posts")
print(response.json())


import pytest
import requests

@pytest.fixture
def api_base_url():
    return "https://jsonplaceholder.typicode.com"

def test_get_posts(api_base_url):
    response = requests.get(f"{api_base_url}/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list







