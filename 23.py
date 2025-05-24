import requests

data = {
    "title": "Hello worlds",
    "body": "This is a post",
    "userId": 1
}
response = requests.options("https://jsonplaceholder.typicode.com/posts/1", json=data)
print(response.status_code)
print(response.headers.get('Access-Control-Allow-Methods'))
# print(response.json())