import io
import cv2
import base64
import requests


from PIL import Image


# A1111 URL
url = "http://192.168.0.75"
# url = "http://192.168.0.135:8899"

# Read Image in RGB order
img = cv2.imread('sd-api-caller/sample_girl.png')

# save img as "debug_depth.png"
cv2.imwrite('sd-api-caller/debug_depth.png', img)



 


# Encode into PNG and send to ControlNet
retval, bytes = cv2.imencode('.png', img)
encoded_image = base64.b64encode(bytes).decode('utf-8')

# A1111 payload
payload = {
  "init_images": [encoded_image],
  "sampler_name": "Euler",
  "alwayson_scripts": {
    "controlnet": {
      "args": [
        {
          "module": "depth_leres",
          "model": "control_v11f1p_sd15_depth [cfd03158]",
          "control_mode": 2
        }
      ]
    }
  }
}
# Trigger Generation
response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)

# Read results
r = response.json()
print(r)
result = r['images'][0]
image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
image.save('sd-api-caller/i2i-output.png')

#save json
import json
with open('sd-api-caller/output.json', 'w') as f:
    dump = json.dumps(r, indent=4)
    f.write(dump)
    f.close()

