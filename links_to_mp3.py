import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def clean_link(link):
    if "youtube.com" in link or "youtu.be" in link:
        return link.split("&")[0]
    elif "soundcloud.com" in link:
        return link.split("?")[0]
    return link

def download_link(url):
    print(f"--- Downloading: {url} ---")
    subprocess.run([
        "yt-dlp", "-x",
        "--audio-format", "mp3",
        "--embed-metadata",
        "--cookies-from-browser", "brave",
        "--remote-components", "ejs:github",
        "-o", "batch/%(title)s.%(ext)s",
        url
    ])

def download_links(links_file, max_workers=4):
    os.makedirs("batch", exist_ok=True)

    with open(links_file, "r") as f:
        links = []
        for line in f:
            link = line.strip()
            if not link or link.startswith("#"):
                continue
            links.append(clean_link(link))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_link, url): url for url in links}
        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"--- Failed: {url} — {e} ---")

    print("--- All downloads complete! ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_links.py <links_file.txt>")
        sys.exit(1)

    download_links(sys.argv[1])