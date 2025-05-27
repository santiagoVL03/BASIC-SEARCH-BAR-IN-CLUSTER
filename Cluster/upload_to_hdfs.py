import os
import sys
import Utils.functions as utils

VIDEO_PATH = "./videos"
METADATA_PATH = "./metadata"

def upload_to_hdfs_hadoop(local_file, hdfs_directory):
    utils.run_command(f"hadoop fs -put {local_file} {hdfs_directory}")

if __name__ == "__main__":
    supported_video_formats = ['.mp4', '.avi', '.mov', '.mkv', '.mpg']
    supported_metadata_formats = ['.json', '.txt']

    if not os.path.exists(METADATA_PATH):
        print(f"Error: The directory {METADATA_PATH} does not exist.")
        sys.exit(1)
    metadata_files = [f for f in os.listdir(METADATA_PATH)
                      if os.path.isfile(os.path.join(METADATA_PATH, f)) and f.lower().endswith(tuple(supported_metadata_formats))]
    if not metadata_files:
        print("No metadata files found in the specified directory.")
        sys.exit(0)

    if not os.path.exists(VIDEO_PATH):
        print(f"Error: The directory {VIDEO_PATH} does not exist.")
        sys.exit(1)
    video_files = [f for f in os.listdir(VIDEO_PATH)
                   if os.path.isfile(os.path.join(VIDEO_PATH, f)) and f.lower().endswith(tuple(supported_video_formats + supported_metadata_formats))]
    if not video_files:
        print("No video or metadata files found in the specified directory.")
        sys.exit(0)

    hdfs_video_directory = "/"
    hdfs_metadata_directory = "/metadata"
    print("Uploading video files to HDFS...")
    for video in video_files:
        video_path = os.path.join(VIDEO_PATH, video)
        if os.path.isfile(video_path):
            print(f"Uploading {video} to HDFS...")
            upload_to_hdfs_hadoop(video_path, hdfs_video_directory)
            print(f"Uploaded {video} successfully.")
    print("Uploading metadata files to HDFS...")
    for metadata in metadata_files:
        metadata_path = os.path.join(METADATA_PATH, metadata)
        if os.path.isfile(metadata_path):
            print(f"Uploading {metadata} to HDFS...")
            upload_to_hdfs_hadoop(metadata_path, hdfs_metadata_directory)
            print(f"Uploaded {metadata} successfully.")
    print("All files uploaded successfully!")
"""
This script uploads video and metadata files to HDFS using Hadoop commands.
It checks for the existence of the specified directories and files, and uploads them to the specified HDFS directories.
It uses subprocess to run the Hadoop fs -put command for uploading files.
Ensure you have the necessary permissions and Hadoop is properly configured to run this script.
Make sure to have the Hadoop client installed and configured on your system.
This script is designed to upload video and metadata files to HDFS using Hadoop commands.
It checks for the existence of the specified directories and files, and uploads them to the specified HDFS directories.
It uses subprocess to run the Hadoop fs -put command for uploading files.
Ensure you have the necessary permissions and Hadoop is properly configured to run this script.
Make sure to have the Hadoop client installed and configured on your system.
This script uploads video and metadata files to HDFS using Hadoop commands.
It checks for the existence of the specified directories and files, and uploads them to the specified HDFS directories.
It uses subprocess to run the Hadoop fs -put command for uploading files.
Ensure you have the necessary permissions and Hadoop is properly configured to run this script.
Make sure to have the Hadoop client installed and configured on your system.
"""