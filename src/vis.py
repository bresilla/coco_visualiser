import os
import json
import cv2
import time

json_file = ".direnv/dw.json"
image_folder = ".direnv/dataset/wur-agrofoodrobotics/cow_pose/images/"

with open(json_file, 'r') as fcc_file:
    fcc_data = json.load(fcc_file)

images = fcc_data["images"]
current = 0;

for pic in (n for n in range(len(fcc_data['images']))):
    image_path = image_folder + fcc_data["images"][pic]["file_name"]
    image_id = fcc_data["images"][pic]["id"]
    print(image_path)
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    for e in (n for n in fcc_data['annotations'] if n["image_id"] == image_id):
        for p in e["points"]:
            color = (0, 0, 255)
            if p[2] == 1:
                color = (0, 255, 255)
            img = cv2.circle(img, (p[0],p[1]), radius=3, color=color, thickness=2)

        for s in fcc_data["categories"]:
            for s1 in s["skeleton"]:
                img = cv2.line(img, (e["points"][s1[0]-1][0], e["points"][s1[0]-1][1]), (e["points"][s1[1]-1][0], e["points"][s1[1]-1][1]), (255, 255, 0), 1)

    cv2.imshow("cows", img)
    cv2.moveWindow("cows", 0, 0)
    k = cv2.waitKey()
    cv2.destroyAllWindows()
    cv2.waitKey(0)
    time.sleep(1)
    print(image_path)