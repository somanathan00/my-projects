import requests
from datetime import datetime
TOKEN = "adfsjasffdjsalfj1"
USERNAME = "somanathan"
GRAPH_ID = "graph2"
pixel_endpoint = "https://pixe.la/v1/users"
params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}
graph_endpoint = f"https://pixe.la/v1/users/{USERNAME}/graphs"
today = datetime.now()
graph_params = {
    "id": GRAPH_ID,
    "name": "progress graph",
    "unit": "hours",
    'type': "int",
    "color": "ajisai"
}
headers = {
    "X-USER-TOKEN": TOKEN
}

pixel_params ={
    "date":today.strftime("%y%m%d"),
    "quantity":"2"
}
pixel_creation = f"{pixel_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
response = requests.post(url=pixel_creation, json=pixel_params, headers=headers)
print(response.text)
