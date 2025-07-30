import time
import subprocess
from pathlib import Path
import sys

SYNC_INTERVAL_MINUTES = 10
CAPTURES_DIR = Path(__file__).parent / 'data' / 'captures'
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
GIT_COMMIT_MESSAGE = 'Auto-sync phone photos (last 2 minutes)'
RECENT_SECONDS = 2 * 60  # 2 minutes
GIT_PATH = r"C:\Program Files\Git\cmd\git.exe"

def is_git_installed():
    try:
        subprocess.run([GIT_PATH, '--version'], check=True, capture_output=True)
        return True
    except Exception:
        return False

def get_recent_image_files():
    if not CAPTURES_DIR.exists():
        print(f"[ERROR] Captures directory does not exist: {CAPTURES_DIR}")
        return []
    now = time.time()
    return [
        f for f in CAPTURES_DIR.iterdir()
        if f.suffix.lower() in IMAGE_EXTENSIONS and f.is_file() and (now - f.stat().st_mtime) <= RECENT_SECONDS
    ]

def git_add_commit_push(files):
    if not files:
        return False
    try:
        subprocess.run([GIT_PATH, 'add'] + [str(f) for f in files], check=True)
        subprocess.run([GIT_PATH, 'commit', '-m', GIT_COMMIT_MESSAGE], check=True)
        subprocess.run([GIT_PATH, 'push'], check=True)
        print(f"[SYNC] Synced {len(files)} new images to git.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git command failed: {e}")
        return False

def main():
    if not is_git_installed():
        print("[FATAL] Git is not installed. Please install Git and try again.")
        sys.exit(1)
    print(f"[INFO] Starting phone photo sync every {SYNC_INTERVAL_MINUTES} minutes (only last 2 minutes of images)...")
    while True:
        recent_images = get_recent_image_files()
        if recent_images:
            if git_add_commit_push(recent_images):
                print(f"[INFO] Synced {len(recent_images)} images taken in the last 2 minutes.")
        else:
            print("[INFO] No new images from the last 2 minutes to sync.")
        time.sleep(SYNC_INTERVAL_MINUTES * 60)

if __name__ == '__main__':
    main()