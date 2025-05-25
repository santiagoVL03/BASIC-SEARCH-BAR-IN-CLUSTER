#!/usr/bin/env python3
import sys

current_class = None
video_set = set()

for line in sys.stdin:
    class_name, path = line.strip().split("\t")
    if current_class != class_name:
        if current_class:
            print(f"{current_class}\t{','.join(sorted(video_set))}")
        current_class = class_name
        video_set = set()
    video_set.add(path)

if current_class:
    print(f"{current_class}\t{','.join(sorted(video_set))}")
