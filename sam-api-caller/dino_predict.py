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
payload = {


    "dino_model_name": "GroundingDINO_SwinT_OGC (694MB)",
    "input_image": filename_to_base64(img_filename).decode(),
    "text_prompt": "clothing",
}
response = requests.post(url, json=payload)
reply = response.json()
print(reply["msg"])

grid = Image.new('RGBA', (512, 512))
paste([reply["image_with_box"]], 0)
grid.show()