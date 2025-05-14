import requests

def check_for_updates(current_version: str):
    """
    Memeriksa versi terbaru dari GitHub repo.
    Jika tersedia versi lebih baru dari current_version, tampilkan notifikasi.
    """

    GITHUB_RAW_URL = "https://raw.githubusercontent.com/k4tedu/Multipjson/main/version.txt"

    try:
        response = requests.get(GITHUB_RAW_URL, timeout=5)
        if response.status_code == 200:
            latest_version = response.text.strip()

            if latest_version != current_version:
                print(f"\n🚀 New version available: {latest_version} (You are using: {current_version})")
                print("🔁 Please update by pulling the latest version from GitHub:")
                print("   git pull origin main\n")
        else:
            print("⚠️ Failed to check for updates (GitHub returned non-200 status).")

    except requests.RequestException as e:
        print(f"⚠️ Unable to check for updates: {e}")
