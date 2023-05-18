import requests
url = "http://192.168.0.75/sam/sam-model"
response = requests.get(url)
reply = response.json()
print(reply)
# Example Output:
# ["sam_vit_b_01ec64.pth", "sam_vit_h_4b8939.pth", "sam_vit_l_0b3195.pth"]