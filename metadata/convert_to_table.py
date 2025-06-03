import json
import csv
import os

metada_dir = "./metadata"
salida_path = "metadata_salida_general.txt"

# Abrimos el archivo de salida una sola vez
with open(salida_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Cabecera con nombre del archivo JSON
    writer.writerow(["archivo_json", "imagen", "class_id", "class_name", "confidence", "x1", "y1", "x2", "y2"])

    for filename in os.listdir(metada_dir):
        if filename.endswith("_detections.json"):
            filepath = os.path.join(metada_dir, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)  # corregido: usabas json.loads(json_data) por error
                    for imagen, objetos in data.items():
                        for obj in objetos:
                            class_id = obj["class_id"]
                            class_name = obj["class_name"]
                            confidence = obj["confidence"]
                            x1, y1, x2, y2 = obj["bbox"]
                            writer.writerow([filename, imagen, class_id, class_name, confidence, x1, y1, x2, y2])
            except json.JSONDecodeError:
                print(f"[!] Error en el archivo JSON: {filename}, se omite.")
                continue
