# controlnet + txt2img
# enable `Allow other script to control this extension` in settings

import base64
import io
import requests
import cv2
from base64 import b64encode
from PIL import Image

def readImage(path):
    img = cv2.imread(path)
    retval, buffer = cv2.imencode('.jpg', img)
    b64img = b64encode(buffer).decode("utf-8")
    return b64img

b64img = readImage("/Users/ming/Downloads/file.png")

class controlnetRequest():
    def __init__(self, prompt):
        self.url = "http://192.168.0.75/sdapi/v1/txt2img"
        self.body = {
            "prompt": prompt,
            "negative_prompt": "",
            "seed": -1,
            "subseed": -1,
            "subseed_strength": 0,
            "batch_size": 1,
            "n_iter": 1,
            "steps": 15,
            "cfg_scale": 7,
            "width": 512,
            "height": 768,
            "restore_faces": True,
            "eta": 0,
            "sampler_index": "Euler a",
            "controlnet_input_image": [b64img],
            "controlnet_module": 'canny',
            "controlnet_model": 'control_canny-fp16 [e3fe7712]',
            "controlnet_guidance": 1.0,
        }

    def sendRequest(self):
        r = requests.post(self.url, json=self.body)
        return r.json()

js = controlnetRequest("walter white").sendRequest()

#print response
print(js)
r = js
print(r)
result = r['images'][0]
image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
image.save('sd-api-caller/output.png')
#save json
with open('sd-api-caller/output.json', 'w') as f:
    f = open('sd-api-caller/output.json', 'w')
    f.write(str(js))
    f.close()
    