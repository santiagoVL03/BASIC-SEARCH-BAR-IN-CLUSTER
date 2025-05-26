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
            video_file = frame_name.split("|")[0] + ".json"
            hdfs_path = f"/hduser/bigdata/nn/{video_file}"
            for obj in detections:
                class_name = obj["class_name"]
                print(f"{class_name}\t{hdfs_path}")
    except Exception as e:
        continue
