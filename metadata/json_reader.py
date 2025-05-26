import json

with open('09162008flight1tape1_3_detections.json', 'r') as f:
    data = json.load(f)  # Esto lee y parsea el contenido JSON del archivo

for frame_name, detections in data.items():
    video_base = frame_name.split("|")[0]
    video_file = video_base.replace(".mpg", "_detections.json")
    hdfs_path = f"/metadata/{video_file}"
    for obj in detections:
        class_name = obj["class_name"]
        print(f"{class_name}\t{hdfs_path}")
