import json
import os

direc = ".direnv/dataset/wur-agrofoodrobotics/cow_pose/releases/dv/annotations/"
impath = ".direnv/dataset/wur-agrofoodrobotics/cow_pose/images/"
json_file = ".direnv/dw.josn"

directory_list = os.listdir(direc)
i = 0;
all = {}
images = {}
annotations = []

for file in directory_list:
    i = i + 1
    pathname, extension = os.path.splitext(file)
    images[str(i)] = pathname + ".jpg"
    with open(direc + file, 'r') as fcc_file:
        fcc_data = json.load(fcc_file)
        for e in fcc_data['annotations']:
            parts = {}
            x_min = int(fcc_data['image']['width'])
            x_max = 0
            y_min = int(fcc_data['image']['height'])
            y_max = 0
            for p in e["skeleton"]["nodes"]:
                if int(p["x"]) < x_min:
                    x_min = int(p["x"])
                if int(p["x"]) > x_max:
                    x_max = int(p["x"])
                if int(p["y"]) < y_min:
                    y_min = int(p["y"])
                if int(p["y"]) > y_max:
                    y_max = int(p["y"])
                parts[p["name"]]=[int(p["x"]),int(p["y"]),int(p["occluded"])]
            width = x_max-x_min
            height = y_max-y_min
            datas = {
                "image_id": i,
                "bbox": [x_min, y_min, width, height],
                "keypoints": [
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
                ],
                "num_keypoints": 20,
                "category_id": 1,
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max,
                "width": width,
                "height": height,
            }
            annotations.append(datas)


categories = { 
    "supercategory": "cow", 
    "id": 1, "name": 
    "cow-skeleton-animal-pose", 
    "keypoints": [ "L_Eye", "R_Eye", "L_EarBase", "R_EarBase", "Nose", "Throat", "TailBase", "Withers", "L_F_Elbow", "R_F_Elbow", "L_B_Elbow", "R_B_Elbow", "L_F_Knee", "R_F_Knee", "L_B_Knee", "R_B_Knee", "L_F_Paw", "R_F_Paw", "L_B_Paw", "R_B_Paw"],
    "skeleton": [[[1, 2], [1, 3], [2, 4], [1, 5], [2, 5], [5, 6], [6, 8], [7, 8], [6, 9], [9, 13], [13, 17], [6, 10], [10, 14], [14, 18], [7, 11], [11, 15], [15, 19], [7, 12], [12, 16], [16, 20]]]
    }

info = {
    "images_path": impath
}

all = {"images": images, "annotations": annotations, "categories": [categories], "info": info}
json_object = json.dumps(all, indent = 4) 
print(json_object)

# with open(json_file, 'w') as f:
#     json.dump(json_object, f)
# f.close()
