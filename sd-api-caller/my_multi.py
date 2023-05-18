import io
import cv2
import base64
import requests


from PIL import Image


# A1111 URL
url = "http://192.168.0.75"
# url = "http://192.168.0.135:8899"

# Read Image in RGB order
canny_img = cv2.imread('sd-api-caller/sample_fullbody.png')[:, :, ::-1]
pose_img = cv2.imread("sd-api-caller/sample_fullbody.png")
#save image as "debug_canny.png"
cv2.imwrite('sd-api-caller/debug_canny.png', canny_img)


# Encode into PNG and send to ControlNet
retval, bytes = cv2.imencode('.png', canny_img)
canny_img_encoded = base64.b64encode(bytes).decode('utf-8')

retval, bytes = cv2.imencode('.png', pose_img)
pose_img_encoded = base64.b64encode(bytes).decode('utf-8')

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

                    "input_image": canny_img_encoded,
                    "module": "canny",
                    "model": "control_v11p_sd15_canny [d14c016b]",
                    # "model": "canny [d14c016b]",
                    
                },
                          {
                    'enabled': True,
                    'low_vram': False,
                    'pixel_perfect': True,

                    "input_image": pose_img_encoded,
                    "module": "openpose",
                    "model": "control_v11p_sd15_openpose [cab727d4]",
                },
                         {
                    'enabled': True,
                    'low_vram': False,
                    'pixel_perfect': True,

                    "input_image": pose_img_encoded,
                    "module": "lineart",
                    "model": "control_v11p_sd15_lineart [43d4be0d]",
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

#save json
import json
with open('sd-api-caller/output.json', 'w') as f:
    dump = json.dumps(r, indent=4)
    f.write(dump)
    f.close()

