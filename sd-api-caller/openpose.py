# controlnet + txt2img
# enable `Allow other script to control this extension` in settings

import base64
import io
import requests
import cv2
from base64 import b64encode
from PIL import Image

# config
prompt = "1girl"
# define mode, if mode = 1, use openpose, if mode = 0, use canny
module_list =  [
    "none",
    "canny",
    "depth",
    "depth_leres",
    "hed",
    "hed_safe",
    "mediapipe_face",
    "mlsd",
    "normal_map",
    "openpose",
    "openpose_hand",
    "openpose_face",
    "openpose_faceonly",
    "openpose_full",
    "clip_vision",
    "color",
    "pidinet",
    "pidinet_safe",
    "pidinet_sketch",
    "pidinet_scribble",
    "scribble_xdog",
    "scribble_hed",
    "segmentation",
    "threshold",
    "depth_zoe",
    "normal_bae",
    "oneformer_coco",
    "oneformer_ade20k",
    "lineart",
    "lineart_coarse",
    "lineart_anime",
    "lineart_standard",
    "shuffle",
    "tile_gaussian",
    "inpaint",
    "invert"
  ]
model_list= [
    "control_v11e_sd15_ip2p [c4bb465c]",
    "control_v11e_sd15_shuffle_2 [526bfdae]",
    "control_v11f1p_sd15_depth [cfd03158]",
    "control_v11p_sd15_canny [d14c016b]",
    "control_v11p_sd15_inpaint [ebff9138]",
    "control_v11p_sd15_lineart [43d4be0d]",
    "control_v11p_sd15_mlsd [aca30ff0]",
    "control_v11p_sd15_normalbae [316696f1]",
    "control_v11p_sd15_openpose [cab727d4]",
    "control_v11p_sd15_scribble [d4ba51ff]",
    "control_v11p_sd15_seg [e1f51eb9]",
    "control_v11p_sd15_softedge [a8575a2a]",
    "control_v11p_sd15s2_lineart_anime [3825e83e]",
    "control_v11u_sd15_tile [1f041471]"
  ]


def readImage(path):
    img = cv2.imread(path)
    retval, buffer = cv2.imencode('.jpg', img)
    b64img = base64.b64encode(buffer).decode("utf-8")
    return b64img

b64img = readImage("sd-api-caller/sample_pose.png")
# Save b64img as debug_openpose.png
with open('sd-api-caller/debug_openpose.png', 'wb') as f:
    img_data = base64.b64decode(b64img)
    f.write(img_data)
    

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
            "height": 512,
            "restore_faces": True,
            "eta": 0,
            "sampler_index": "Euler a",
            "controlnet_input_image": [b64img],
            "controlnet_module": 'openpose',
            "controlnet_model": 'control_v11p_sd15_openpose [cab727d4]',
            "controlnet_guidance": 1.0,
        }

    def sendRequest(self):
        r = requests.post(self.url, json=self.body)
        return r.json()

js = controlnetRequest(prompt).sendRequest()

#print response
print(js)
r = js
result = r['images'][0]
image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
image.save('sd-api-caller/output.png')