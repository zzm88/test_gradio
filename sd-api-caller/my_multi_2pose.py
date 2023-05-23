import io
import cv2
import base64
import requests


from PIL import Image


# A1111 URL
url = "http://192.168.0.75"
# url = "http://192.168.0.135:8899"

# Read Image in RGB order
pose_img = cv2.imread('sd-api-caller/sample/sample_multi_pose_body.png')[:, :, ::-1]
hand_img = cv2.imread("sd-api-caller/sample/sample_multi_pose_hand.png")
#save image as "debug_canny.png"
cv2.imwrite('sd-api-caller/debug/debug_hand.png', hand_img)


# Encode into PNG and send to ControlNet
retval, bytes = cv2.imencode('.png', hand_img)
hand_img_encoded = base64.b64encode(bytes).decode('utf-8')

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
                    'low_vram': False,
                    'pixel_perfect': True,

                    "input_image": pose_img_encoded,
                    # "module": "openpose",
                    "model": "control_v11p_sd15_openpose [cab727d4]",
                    "control_mode":2
                },
                             {
                    'enabled': True,
                    'low_vram': False,
                    'pixel_perfect': True,

                    "input_image": hand_img_encoded,
                    # "module": "openpose",
                    "model": "control_v11p_sd15_openpose [cab727d4]",
                    "control_mode":2
                }, 
    
                
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

