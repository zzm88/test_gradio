def get_model_and_module(mode):
    module_list = [
        "none", "canny", "depth", "depth_leres", "hed", "hed_safe", "mediapipe_face", "mlsd", "normal_map",
        "openpose", "openpose_hand", "openpose_face", "openpose_faceonly", "openpose_full", "clip_vision", "color",
        "pidinet", "pidinet_safe", "pidinet_sketch", "pidinet_scribble", "scribble_xdog", "scribble_hed",
        "segmentation", "threshold", "depth_zoe", "normal_bae", "oneformer_coco", "oneformer_ade20k", "lineart",
        "lineart_coarse", "lineart_anime", "lineart_standard", "shuffle", "tile_gaussian", "inpaint", "invert"
    ]

    model_list = [
        "control_v11e_sd15_ip2p [c4bb465c]", "control_v11e_sd15_shuffle_2 [526bfdae]",
        "control_v11f1p_sd15_depth [cfd03158]", "control_v11p_sd15_canny [d14c016b]",
        "control_v11p_sd15_inpaint [ebff9138]", "control_v11p_sd15_lineart [43d4be0d]",
        "control_v11p_sd15_mlsd [aca30ff0]", "control_v11p_sd15_normalbae [316696f1]",
        "control_v11p_sd15_openpose [cab727d4]", "control_v11p_sd15_scribble [d4ba51ff]",
        "control_v11p_sd15_seg [e1f51eb9]", "control_v11p_sd15_softedge [a8575a2a]",
        "control_v11p_sd15s2_lineart_anime [3825e83e]", "control_v11u_sd15_tile [1f041471]"
    ]

    mapping = dict(zip(module_list, model_list))

    # Get the appropriate model and module with the given mode
    if mode in mapping:
        model_and_module = mapping[mode]
        model, module = model_and_module.split(" [")
        module = module[:-1]
        print("Mode:", mode)
        print("Model:", model)
        print("Module:", module)
        module_and_model = [module, model]
    else:
        print("No mapping found for the mode:", mode)
        module_and_model = []

    return module_and_model


# Example usage
mode = "openpose"
module_and_model = get_model_and_module(mode)
print(module_and_model)