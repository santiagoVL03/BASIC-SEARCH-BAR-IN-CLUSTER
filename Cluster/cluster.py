import asyncio
import os
import re
import Utils.functions as utils
import sys

def run_scrapper():
    """Run the scrapper downloader script."""
    try:
        utils.run_command("python3 -m Utils.scrapper_downloader_video")
    except Exception as e:
        print(f"Error running scrapper downloader: {e}")
        raise
    finally:
        print("Scrapper downloader script completed.")

def run_process_video():
    """Run the process video script."""
    try:
        utils.run_command("python3 -m Src.process_video")
    except Exception as e:
        print(f"Error running process video: {e}")
        raise
    finally:
        print("Process video script completed.")

def run_upload_to_hdfs():
    """Run the upload to HDFS script."""
    try:
        utils.run_command("python3 -m Cluster.upload_to_hdfs")
    except Exception as e:
        print(f"Error running upload to HDFS: {e}")
        raise
    finally:
        print("Upload to HDFS script completed.")

def main():
    """Main function to run all scripts in sequence."""
    print("Starting scrapper downloader...")
    run_scrapper()
    
    print("Starting process video...")
    run_process_video()
    
    print("Starting upload to HDFS...")
    run_upload_to_hdfs()
    
    print("All scripts completed successfully.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        print("Script execution finished.")