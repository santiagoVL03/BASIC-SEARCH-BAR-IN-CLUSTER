import os
import json

metadata_dir = "./metadata"

for filename in os.listdir(metadata_dir):
    if filename.endswith("_detections_standalone.json"):
        filepath = os.path.join(metadata_dir, filename)
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            continue  # Ignora archivos con errores de formato JSON

        # Sobrescribe el archivo con una versión compacta (1 línea)
        with open(filepath, "w") as f:
            json.dump(data, f, separators=(",", ":"))