import matplotlib.pyplot as plt
import cv2
import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr.strip()}")
        sys.exit(1)


def display_image(image, title="Image"):
    """
    Display an image using matplotlib.
    
    Parameters:
    - image: The image to display (numpy array).
    - title: Title of the displayed image.
    """

    plt.imshow(image)
    plt.title(title)
    plt.axis('off')
    plt.show()
    
def resize_image(image, new_size):
    """
    Resize an image to a new size.
    
    Parameters:
    - image: The image to resize (numpy array).
    - new_size: Tuple of (width, height) for the new size.
    
    Returns:
    - Resized image (numpy array).
    """
    return cv2.resize(image, new_size)

def get_video_fps(video_path):
    """
    Get the frames per second (FPS) of a video.
    
    Parameters:
    - video_path: Path to the video file.
    
    Returns:
    - FPS of the video (float).
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps

def convert_video_to_frames(video_path, output_dir, frame_skip=24):
    """
    Convert a video to frames and save them to a directory.
    
    Parameters:
    - video_path: Path to the video file.
    - output_dir: Directory to save the frames.
    - frame_skip: Number of frames to skip (default is 1).
    """
    cap = cv2.VideoCapture(video_path)
    video_name = os.path.basename(video_path)
    frame_count = 0
    os.makedirs(output_dir, exist_ok=True)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_skip == 0:
            frame_name = os.path.join(output_dir, f"{video_name}|_frame_{frame_count}.jpg")
            cv2.imwrite(frame_name, frame)
        frame_count += 1
    cap.release()