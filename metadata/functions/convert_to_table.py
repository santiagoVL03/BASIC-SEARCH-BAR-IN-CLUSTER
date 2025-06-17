import json
import csv
import os

metada_dir = "./metadata"
salida_path = "metadata/metadata_salida_general.txt"
videos_path = "metadata/lista_videos.txt"

def extraer_video_id(nombre_json):
    return nombre_json.replace("_detections.json", "")

def extraer_frame(nombre_imagen):
    try:
        frame_part = nombre_imagen.split("_frame_")[1]
        return frame_part.replace(".jpg", "")
    except IndexError:
        return "unknown"

video_ids_unicos = set()

with open(salida_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["video_id", "frame", "class_id", "class_name", "confidence", "x1", "y1", "x2", "y2"])

    for filename in os.listdir(metada_dir):
        if filename.endswith("_detections.json"):
            filepath = os.path.join(metada_dir, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    video_id = extraer_video_id(filename)
                    video_ids_unicos.add(video_id)
                    for imagen, objetos in data.items():
                        frame = extraer_frame(imagen)
                        for obj in objetos:
                            class_id = obj["class_id"]
                            class_name = obj["class_name"]
                            confidence = obj["confidence"]
                            x1, y1, x2, y2 = obj["bbox"]
                            writer.writerow([video_id, frame, class_id, class_name, confidence, x1, y1, x2, y2])
            except json.JSONDecodeError:
                print(f"[!] Error en el archivo JSON: {filename}, se omite.")
                continue

# with open(videos_path, mode="w") as f_vid:
#     for vid in sorted(video_ids_unicos):
#         f_vid.write(vid + "\n")
