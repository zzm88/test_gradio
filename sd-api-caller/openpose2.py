import io
import cv2
import base64
import requests


from PIL import Image


# A1111 URL
url = "http://192.168.0.75"

# sample from Mikubill/sd-webui-controlnet/wiki/API

# Read Image in RGB order
img = cv2.imread("sd-api-caller/sample_pose.png")
cv2.imwrite('sd-api-caller/debug_openpose.png', img)

# Encode into PNG and send to ControlNet
retval, bytes = cv2.imencode('.png', img)
encoded_image = base64.b64encode(bytes).decode('utf-8')

# A1111 payload
payload = {
    "prompt": '1man',
    "negative_prompt": "",
    "batch_size": 1,
    "steps": 20,
    "cfg_scale": 7,
    "alwayson_scripts": {
        "controlnet": {
            "args": [
                {
                    'enabled': True,
                    'low_vram': False,
                    'pixel_perfect': True,

                    "input_image": encoded_image,
                    # "module": "openpose",
                    "model": "control_v11p_sd15_openpose [cab727d4]",
                }
            ]
        }
    }
}


# Trigger Generation
response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

# Read results
r = response.json()
print(r)
result = r['images'][0]
image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
image.save('sd-api-caller/output.png')