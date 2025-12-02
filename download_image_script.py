import os
import requests
from urllib.parse import urlparse
from pathlib import Path

 # Get the directory where this script is located, then find 'data' inside it
BASE_DIR = Path(__file__).resolve().parent / "data"
WITH_DIR = BASE_DIR / "with_logo"
WITHOUT_DIR = BASE_DIR / "without_logo"

WITH_URL_FILE = BASE_DIR / "with_logo_urls.txt"
WITHOUT_URL_FILE =BASE_DIR / "without_logo_urls.txt"


def safe_extension_from_url(url: str) -> str:
    """
    Try to keep the original extension; fall back to .jpg if unknown.
    """
    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower()
    if ext in [".jpg", ".jpeg", ".png"]:
        return ext
    return ".jpg"


def download_from_list(url_file: str, out_dir: Path, prefix: str):
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(url_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for idx, url in enumerate(lines, start=1):
        ext = safe_extension_from_url(url)
        filename = f"{prefix}_{idx:03d}{ext}"
        out_path = out_dir / filename

        print(f"[{prefix}] Downloading {idx}/{len(lines)}: {url}")
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            with open(out_path, "wb") as img_file:
                img_file.write(resp.content)
        except Exception as e:
            print(f"   Failed: {e}")


def main():
    if os.path.exists(WITH_URL_FILE):
        download_from_list(WITH_URL_FILE, WITH_DIR, "with")
    else:
        print(f"Warning: {WITH_URL_FILE} not found.")

    if os.path.exists(WITHOUT_URL_FILE):
        download_from_list(WITHOUT_URL_FILE, WITHOUT_DIR, "without")
    else:
        print(f"Warning: {WITHOUT_URL_FILE} not found.")

    print("Done. Check the data folders.")


if __name__ == "__main__":
    main()
