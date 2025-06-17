import subprocess
def create_all_logs():
    """
    Create all logs by running the create_all_logs.sh script.
    """
    try:
        subprocess.run(["bash", "hive/auto/create_all_logs.sh"], check=True)
        print("All logs created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating logs: {e}")