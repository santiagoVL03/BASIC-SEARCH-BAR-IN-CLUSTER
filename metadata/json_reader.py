import os
import json

metadata_dir = "./metadata"
output_items = []

for filename in os.listdir(metadata_dir):
    if filename.endswith("_detections.json"):
        filepath = os.path.join(metadata_dir, filename)
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue  # Ignorar archivos con formato incorrecto

        for frame_name, detections in data.items():
            video_base = frame_name.split("|")[0]
            video_file = video_base.replace(".mpg", "_detections.json")
            hdfs_path = f"/metadata/{video_file}"
            for obj in detections:
                class_name = obj.get("class_name")
                if class_name:
                    output_items.append(f"{class_name}\t{hdfs_path}")

print(" ".join(output_items))
output_json_path = os.path.join(metadata_dir, "json_reader.json")
with open(output_json_path, "w") as f:
    json.dump(output_items, f, indent=4)
