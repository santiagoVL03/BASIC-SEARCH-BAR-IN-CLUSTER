#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        data = line.split("\t", 1)[1]
        print(data)
    except Exception as e:
        continue
