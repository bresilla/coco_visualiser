import datetime
import random
import json
import os

direc = "/home/bresilla/.darwin/datasets/wur-agrofoodrobotics/cow_pose/releases/newr/annotations/"
impath = "/home/bresilla/.darwin/datasets/wur-agrofoodrobotics/cow_pose/images/"
json_file = "/home/bresilla/.darwin/datasets/wur-agrofoodrobotics/cow_pose/releases/newr/"

directory_list = os.listdir(direc)
random.shuffle(directory_list)

split=int((len(directory_list)/10)*8)
data_list = [{"images": directory_list[:split], "name": "train.json"}, {"images": directory_list[split:], "name": "val.json"}]

for coll in data_list:
    images = []
    annotations = []
    i = random.randint(11111, 99999);
    for file in coll["images"]:
        i = i + 1
        with open(direc + file, 'r') as fcc_file:
            fcc_data = json.load(fcc_file)
            image_struct = {
                "id": i,
                "file_name": fcc_data["image"]["original_filename"],
                "width": int(fcc_data['image']['width']),
                "height": int(fcc_data['image']['height']),
                "full_name": impath + fcc_data["image"]["original_filename"],
            }
            images.append(image_struct)
            for e in fcc_data['annotations']:
                img_width=int(fcc_data['image']['width'])
                img_height=int(fcc_data['image']['height'])
                parts = {}
                x_min = img_width
                x_max = 0
                y_min = img_height
                y_max = 0
                for p in e["skeleton"]["nodes"]:
                    if int(p["x"]) < x_min:
                        x_min = int(p["x"])
                        if x_min < 0: x_min = 0
                    if int(p["x"]) > x_max:
                        x_max = int(p["x"])
                        if x_max > img_width: x_max + img_width
                    if int(p["y"]) < y_min:
                        y_min = int(p["y"])
                        if y_min < 0: y_min = 0
                    if int(p["y"]) > y_max:
                        y_max = int(p["y"])
                        if y_max > img_height: y_max + img_height
                    parts[p["name"]]=[int(p["x"]),int(p["y"]),int(p["occluded"])+1]
                ann_width = x_max-x_min
                ann_height = y_max-y_min
                keypoints = [
                        parts["left_eye"],
                        parts["right_eye"],
                        parts["left_ear"],
                        parts["right_ear"],
                        parts["nose"],
                        parts["throat"],
                        parts["tailbase"],
                        parts["withers"],
                        parts["front_left_elbow"],
                        parts["front_right_elbow"],
                        parts["rear_left_elbow"],
                        parts["rear_right_elbow"],
                        parts["front_left_knee"],
                        parts["front_right_knee"],
                        parts["rear_left_knee"],
                        parts["rear_right_knee"],
                        parts["front_left_paw"],
                        parts["front_right_paw"],
                        parts["rear_left_paw"],
                        parts["rear_right_paw"],
                    ]
                datas = {
                    "keypoints": [float(item) for sub_list in keypoints for item in sub_list],
                    "image_id": i,
                    "id": e["instance_id"]["value"],
                    "num_keypoints": 20,
                    "bbox": [float(x_min), float(y_min), float(ann_width), float(ann_height)],
                    "iscrowd": 0,
                    "area": float(ann_width * ann_height),
                    "category_id": 1,
                    "x_min": x_min,
                    "x_max": x_max,
                    "y_min": y_min,
                    "y_max": y_max,
                    "width": ann_width,
                    "height": ann_height,
                    "points": keypoints,
                }
                annotations.append(datas)


    categories = { 
        "supercategory": "animal",
        "id": 1,
        "name": "cow",
        "keypoints": [ "L_Eye", "R_Eye", "L_EarBase", "R_EarBase", "Nose", "Throat", "TailBase", "Withers", "L_F_Elbow", "R_F_Elbow", "L_B_Elbow", "R_B_Elbow", "L_F_Knee", "R_F_Knee", "L_B_Knee", "R_B_Knee", "L_F_Paw", "R_F_Paw", "L_B_Paw", "R_B_Paw"],
        "skeleton": [[1, 2], [1, 3], [2, 4], [1, 5], [2, 5], [5, 6], [6, 8], [7, 8], [6, 9], [9, 13], [13, 17], [6, 10], [10, 14], [14, 18], [7, 11], [11, 15], [15, 19], [7, 12], [12, 16], [16, 20]]
        }

    info = {
        "version": "1.0",
        "data_path": impath,
        "date_created": str(datetime.datetime.now()),
        "dataset_size": len(coll["images"])
    }

    all = {"info": info, "images": images, "annotations": annotations, "categories": [categories]}
    json_object = json.dumps(all, indent = 4) 
    name = json_file+coll["name"]
    with open(name, 'w') as f:
        f.write(json_object)
