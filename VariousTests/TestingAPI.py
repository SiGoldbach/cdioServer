# This file can be used to test the server and see if a valid response is returned by the endpoint test with given URL.

import Moves
import json

import requests

url = 'http://192.168.198.237:5000/test'

print("Testing API")
response = requests.get(url)

# Here response.text needs to be used then it is transformed into a string and not a dict
print(response.text)

move = json.loads(response.text, object_hook=Moves.as_payload)

# move.print()
