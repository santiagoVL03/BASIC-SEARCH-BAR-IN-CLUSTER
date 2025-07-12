from ultralytics import YOLO
import os, json, sys
import Utils.functions as utils
from pathlib import Path

VIDEO_PATH = Path("./videos")
METADATA_PATH = Path("./metadata")
VIDEO_FILES = []
MODEL = YOLO("yolov8n.pt")

def process_standalone_video (video_name: str):
    supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.mpg']
    if not os.path.exists(VIDEO_PATH):
        print(f"Error: The directory {VIDEO_PATH} does not exist.")
        sys.exit(1)
        
    VIDEO_PATH.mkdir(exist_ok=True)
    METADATA_PATH.mkdir(exist_ok=True)
    
    VIDEO_FILE_PATH = os.path.join(VIDEO_PATH, video_name)
    if not os.path.isfile(VIDEO_FILE_PATH) or not video_name.lower().endswith(tuple(supported_formats)):
        print(f"Error: The file {VIDEO_FILE_PATH} does not exist or is not a supported video format.")
        sys.exit(1)
    
    print(f"Processing video: {VIDEO_FILE_PATH}")
    fps = utils.get_video_fps(VIDEO_FILE_PATH)
    print(f"FPS: {fps}")
    output_dir = os.path.join(VIDEO_PATH, "frames", os.path.splitext(video_name)[0])
    utils.convert_video_to_frames(VIDEO_FILE_PATH, output_dir, frame_skip=100)
    output_json_path = os.path.join(METADATA_PATH, f"{os.path.splitext(video_name)[0]}_detections_standalone.json")
    if os.path.exists(output_json_path):
        print(f"Skipping {video_name}, already processed.")
        return
    
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_name = sys.argv[1]
        process_standalone_video(video_name)
    else:
        print("Usage: python process_standalone_video.py <video_name>")
        print("Example: python process_standalone_video.py my_video.mp4")