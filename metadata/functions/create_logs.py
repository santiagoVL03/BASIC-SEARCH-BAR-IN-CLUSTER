import csv
import os
import random
from datetime import datetime, timedelta

metadata_dir = "./metadata"
input_path = "metadata/lista_videos.txt"

user_names = [
    "kawaii", "tenten", "puck", "siri",
    "ricky", "momo", "kiki", "luna",
    "nina", "toto", "lili", "bubu", "dodo", "fifi", "gigi", "huhu"
]


def generate_random_datetime():
    start_date = datetime(2024, 6, 1)
    end_date = datetime(2024, 6, 16)
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

def generate_random_user():
    return random.choice(user_names) + "_" + random.choice(user_names) + "-" + str(random.randint(1, 1000))

def create_logs(input_path, output_path):
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)

    with open(input_path, "r") as infile:
        video_list = [line.strip() for line in infile.readlines()]

    logs = []
    for _ in range(200):
        user = generate_random_user()
        timestamp = generate_random_datetime().strftime("%Y-%m-%d %H:%M:%S")
        video = random.choice(video_list)
        logs.append([user, timestamp, video])

    with open(output_path, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(logs)

output_path = os.path.join(metadata_dir, "logs_system.txt")
create_logs(input_path, output_path)