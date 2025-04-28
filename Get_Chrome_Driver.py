#JSpectre
import os
import platform
import re
import requests
import zipfile
import shutil
from pathlib import Path
import subprocess

def get_chrome_version():
    system = platform.system()
    if system == "Windows":
        try:
            result = subprocess.run(
                r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                shell=True
            )
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)", result.stdout)
            return match.group(1) if match else None
        except:
            return None
    elif system == "Linux":
        result = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True)
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", result.stdout)
        return match.group(1) if match else None
    elif system == "Darwin":  # macOS
        result = subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"], capture_output=True, text=True)
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", result.stdout)
        return match.group(1) if match else None
    return None

def download_chromedriver(chrome_version, target_path="drivers"):
    major_version = chrome_version.split(".")[0]
    latest_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
    latest_version = requests.get(latest_url).text.strip()

    system = platform.system()
    arch = platform.machine()

    if system == "Windows":
        zip_name = "chromedriver-win32.zip"
    elif system == "Linux":
        zip_name = "chromedriver-linux64.zip"
    elif system == "Darwin":
        zip_name = "chromedriver-mac-x64.zip" if arch == "x86_64" else "chromedriver-mac-arm64.zip"
    else:
        raise Exception("Unsupported OS")

    dl_url = f"https://chromedriver.storage.googleapis.com/{latest_version}/{zip_name}"
    os.makedirs(target_path, exist_ok=True)
    zip_path = os.path.join(target_path, zip_name)

    print(f"Downloading ChromeDriver {latest_version} for {system}...")
    with requests.get(dl_url, stream=True) as r:
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    # Extract zip
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(target_path)

    # Clean up zip
    os.remove(zip_path)
    return os.path.join(target_path, "chromedriver.exe" if system == "Windows" else "chromedriver")

# --- Usage Example ---
if __name__ == "__main__":
    chrome_ver = get_chrome_version()
    if chrome_ver:
        driver_path = download_chromedriver(chrome_ver)
        print(f"Driver downloaded to: {driver_path}")
    else:
        print("Could not determine Chrome version. Please ensure Chrome is installed.")
