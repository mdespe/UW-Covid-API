import requests

response = requests.get('https://infinite-shore-86765.herokuapp.com/uw-covid')
print(response.text)