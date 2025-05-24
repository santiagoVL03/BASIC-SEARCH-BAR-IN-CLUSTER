import cv2
import json
import os
import sys
from ultralytics import YOLO
from Utils import functions

VIDEO_PATH = "videos"
VIDEO_FILES = []
if __name__ == "__main__":
    # Get all video files from the VIDEO_PATH directory
    
    supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.mpg']  # Add more formats if needed

    if not os.path.exists(VIDEO_PATH):
        print(f"Error: The directory {VIDEO_PATH} does not exist.")
        sys.exit(1)

    # List all files in the video directory
    for file in os.listdir(VIDEO_PATH):
        file_path = os.path.join(VIDEO_PATH, file)
        if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in supported_formats):
            VIDEO_FILES.append(file)

    print(f"Found {len(VIDEO_FILES)} video files: {VIDEO_FILES}")