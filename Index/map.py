#!/usr/bin/env python3
import sys
import json
import os

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        data = json.loads(line)
        for frame_name, detections in data.items():
            video_base = frame_name.split("|")[0]
            video_file = os.path.basename(video_base).replace(".mpg", "_detections.json")
            hdfs_path = f"/metadata/{video_file}"
            for obj in detections:
                class_name = obj["class_name"]
                print(f"{class_name}\t{hdfs_path}")
    except Exception as e:
        print(f"Mapper error: {e}", file=sys.stderr)
