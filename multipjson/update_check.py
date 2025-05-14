import requests
import os

def check_for_updates():
    try:
        version_file = os.path.join(os.path.dirname(__file__), "version.txt")
        with open(version_file, 'r') as f:
            local_version = f.read().strip()

        response = requests.get("https://raw.githubusercontent.com/k4tedu/Multipjson/main/multipjson/version.txt")
        if response.status_code == 200:
            remote_version = response.text.strip()
            if remote_version != local_version:
                print(f"\n🔔 Update available: {remote_version} (you have {local_version})")
                print("👉 Run `git pull` or re-clone from GitHub to get the latest version.\n")
    except Exception:
        pass  # Silent if offline
