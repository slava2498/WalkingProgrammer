import requests

data = {
    "title": "Hello",
    "body": "This is a post",
    "userId": 1
}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=data)
print(response.status_code)
print(response.json())