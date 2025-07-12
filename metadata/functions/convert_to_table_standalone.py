import json
import csv
import os
import sys

# Validar argumento
if len(sys.argv) < 2:
    print("Uso: python procesar_metadata.py <nombre_archivo_json>")
    sys.exit(1)

# Ruta al archivo JSON a procesar
nombre_json = sys.argv[1]

# Rutas
metadata_dir = "./metadata"
salida_path = os.path.join(metadata_dir, "metadata_salida_general.txt")
filepath = os.path.join(metadata_dir, nombre_json)

# Extraer ID de video desde el nombre del archivo
def extraer_video_id(nombre_json):
    return nombre_json.replace("_detections_standalone.json", "")

# Extraer número de frame desde nombre de imagen
def extraer_frame(nombre_imagen):
    try:
        frame_part = nombre_imagen.split("_frame_")[1]
        return frame_part.replace(".jpg", "")
    except IndexError:
        return "unknown"

# Procesamiento
video_id = extraer_video_id(nombre_json)

try:
    with open(filepath, "r") as f:
        data = json.load(f)
except json.JSONDecodeError:
    print(f"[!] Error al leer el archivo JSON: {nombre_json}")
    sys.exit(1)

# Abrir archivo de salida en modo append (añadir al final)
with open(salida_path, mode="a", newline="") as file:
    writer = csv.writer(file)
    for imagen, objetos in data.items():
        frame = extraer_frame(imagen)
        for obj in objetos:
            class_id = obj["class_id"]
            class_name = obj["class_name"]
            confidence = obj["confidence"]
            x1, y1, x2, y2 = obj["bbox"]
            writer.writerow([video_id, frame, class_id, class_name, confidence, x1, y1, x2, y2])

print(f"[✓] Procesamiento completado para: {nombre_json}")


# with open(videos_path, mode="w") as f_vid:
#     for vid in sorted(video_ids_unicos):
#         f_vid.write(vid + "\n")
