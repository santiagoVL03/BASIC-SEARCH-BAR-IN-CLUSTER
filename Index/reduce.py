#!/usr/bin/env python3
import sys
from collections import defaultdict

counts = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    video_name, class_name = line.split('\t')
    key = (video_name, class_name)
    counts[key] += 1

# imprimir todos los conteos
for (video_name, class_name), count in counts.items():
    print(f"{video_name}\t{class_name}\t{count}")
