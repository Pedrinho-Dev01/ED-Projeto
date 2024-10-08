import requests

default = 'https://arquivo.pt/textsearch?q='
election_time = '&from=20200203000000&to=20201103000000'
non_election_time = '&from=20180203000000&to=20181103000000'

def request_api(query, is_election):
    if query:

        if is_election == 1:
            response = requests.get(default + query + election_time)
            return response
        elif is_election == 0:
            response = requests.get(default + query + non_election_time)
            return response
    else:
        print("No query provided")
        return
    
input_query = input("Enter a query: ")
is_election = int(input("Is it election time? (1 for yes, 0 for no): "))
response = request_api(input_query, is_election)

# relevant results are in response_items
response_items = response.json()['response_items']
# save the response_items to a file response_items.json
with open('response_items.json', 'w') as f:
    f.write(str(response_items))
    f.close()
