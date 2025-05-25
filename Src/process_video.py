from ultralytics import YOLO
import os, json, sys
import Utils.functions as utils
from pathlib import Path

VIDEO_PATH = Path("./videos")
METADATA_PATH = Path("./metadata")
VIDEO_FILES = []
MODEL = YOLO("yolov8n.pt")

if __name__ == "__main__":
    supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.mpg']
    if not os.path.exists(VIDEO_PATH):
        print(f"Error: The directory {VIDEO_PATH} does not exist.")
        sys.exit(1)

    VIDEO_PATH.mkdir(exist_ok=True)

    VIDEO_FILES = [f for f in os.listdir(VIDEO_PATH)
                   if os.path.isfile(os.path.join(VIDEO_PATH, f)) and f.lower().endswith(tuple(supported_formats))]

    for video in VIDEO_FILES:
        video_file = os.path.splitext(video)[0]
        video_path = os.path.join(VIDEO_PATH, video)
        print(f"Processing video: {video_path}")
        fps = utils.get_video_fps(video_path)
        print(f"FPS: {fps}")

        output_dir = os.path.join(VIDEO_PATH, "frames", os.path.splitext(video)[0])
        utils.convert_video_to_frames(video_path, output_dir, frame_skip=100)

        output_json_path = os.path.join(METADATA_PATH, f"{video_file}_detections.json")
        if os.path.exists(output_json_path):
            print(f"Skipping {video}, already processed.")
            continue

        all_results = {}
        for frame_file in sorted(os.listdir(output_dir)):
            frame_path = os.path.join(output_dir, frame_file)
            try:
                results = MODEL(frame_path)
            except Exception as e:
                print(f"Failed on {frame_file}: {e}")
                continue

            detections = []
            for result in results:
                for box in result.boxes:
                    xyxy = box.xyxy[0].tolist()
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = result.names[cls_id]
                    detections.append({
                        "class_id": cls_id,
                        "class_name": class_name,
                        "confidence": conf,
                        "bbox": xyxy
                    })

            all_results[frame_file] = detections

        with open(output_json_path, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"\n✔️ JSON saved: {output_json_path}")

    if not VIDEO_FILES:
        print("No video files found.")
    else:
        print(f"Found {len(VIDEO_FILES)} video files: {VIDEO_FILES}")
