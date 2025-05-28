#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    data = json.loads(line)
    for video_frame, detections in data.items():
        video_name = video_frame.split('|')[0]
        for obj in detections:
            class_name = obj.get("class_name")
            if class_name:
                # Emitir como clave única: video_name \t class_name
                print(f"{video_name}\t{class_name}")
