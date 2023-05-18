import requests
from PIL import Image
url = "http://192.168.0.75/sam/dino-predict"
import base64
from io import BytesIO
img_filename = "sam-api-caller/sample_canny.png"

def filename_to_base64(filename):
    with open(filename, "rb") as fh:
        return base64.b64encode(fh.read())

def paste(img, row):
    for idx, img in enumerate(img):
        img_pil = Image.open(BytesIO(base64.b64decode(img))).resize((512, 512))
        grid.paste(img_pil, (idx * 512, row * 512))
        
url = "http://192.168.0.75/sam/dilate-mask"
payload = {
    "input_image": filename_to_base64(img_filename).decode(),
    "mask": reply["mask"],
}
response = requests.post(url, json=payload)
reply = response.json()

grid = Image.new('RGBA', (3 * 512, 512))
paste([reply["blended_image"], reply["mask"], reply["masked_image"]], 0)
grid.show()