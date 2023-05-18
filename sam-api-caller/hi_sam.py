import requests
url = "http://192.168.0.75/sam/heartbeat" 
response = requests.get(url)
reply = response.json()
print(reply["msg"])