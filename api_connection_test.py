import requests

def request_api(q):
    if q:
        response = requests.get('https://arquivo.pt/textsearch?q=' + q)
    else:
        response = requests.get('https://arquivo.pt/textsearch?q=default')
    return response

# api response is a json object
input_query = input("Enter a query: ")
response = request_api()
print(response.json())