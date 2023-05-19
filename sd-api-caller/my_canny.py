import io
import random
import cv2
import base64
import requests


from PIL import Image


# A1111 URL
url = "http://192.168.0.75"
# url = "http://192.168.0.135:8899"

#list files under sam-api-caller/output
import os
filelist = (os.listdir("sd-api-caller/raw/"))
for file in filelist:
    img_filename = "sd-api-caller/raw/"+file

# Read Image in RGB order
img = cv2.imread(img_filename)[:, :, ::-1]
#save image as "debug_canny.png"
cv2.imwrite('sd-api-caller/debug_canny.png', img)


# Encode into PNG and send to ControlNet
retval, bytes = cv2.imencode('.png', img)
encoded_image = base64.b64encode(bytes).decode('utf-8')

# A1111 payload
payload = {
    "prompt": '',
    "negative_prompt": "",
    "batch_size": 1,
    "steps": 20,
    "cfg_scale": 7,
    "alwayson_scripts": {
        "controlnet": {
            "args": [
                {
                    'enabled': True,
                    # 'low_vram': False,
                    'pixel_perfect': True,

                    "input_image": encoded_image,
                    "module": "canny",
                    "model": "control_v11p_sd15_canny [d14c016b]",
                    # "model": "canny [d14c016b]",
                }
            ]
        }
    }
}

# Trigger Generation
def run_canny():
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    # Read results
    r = response.json()
    print(r)
    result = r['images'][0]
    image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
    rnd_id = str(random.randint(0, 100000))
    image.save('sd-api-caller/'+ 'out/'+ rnd_id + '.png')
    #save json
    import json
    with open('sd-api-caller/out{rnd_id}_log.json', 'w') as f:
        dump = json.dumps(r, indent=4)
        f.write(dump)
        f.close()

for i in range(0, 10):
    run_canny()