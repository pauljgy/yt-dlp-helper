import csv
import subprocess
import sys
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def search_youtube(query, max_duration=600):
    SKIP_KEYWORDS = ["music video", "m/v", "mv", "video", "stream", "live", "visual"]

    result = subprocess.run(
        ["yt-dlp", f"ytsearch5:{query}", "--dump-json", "--no-playlist",
        "--remote-components", "ejs:github",
        "--cookies-from-browser", "brave"],
        capture_output=True, text=True
    )

    for line in result.stdout.strip().splitlines():
        try:
            video = json.loads(line)
            title = video.get("title", "").lower()
            duration = video.get("duration", 0)

            if any(keyword in title for keyword in SKIP_KEYWORDS):
                print(f"  ⏭ Skipping '{video.get('title', 'unknown')}' (music video)")
                continue

            if duration and duration <= max_duration:
                print(f"  \033[1;92m✓ Matched: '{title}'\033[0m")
                return f"https://www.youtube.com/watch?v={video['id']}"
            else:
                print(f"  ⏭ Skipping '{video.get('title', 'unknown')}' (duration: {duration//60}m {duration%60}s)")
        except json.JSONDecodeError:
            continue

    return None

def search_song(row):
    title = row.get("Name", "").strip()
    artist = row.get("Artist", "").strip()
    if not title:
        return None, None, None

    query = f"{artist} {title} extended mix"
    print(f"Searching: {query}")
    url = search_youtube(query)
    return title, artist, url

def playlist_to_youtube_links(playlist_file, output_file, max_workers=5):
    with open(playlist_file, "r", encoding="utf-16") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    results = [None] * len(rows)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {executor.submit(search_song, row): i for i, row in enumerate(rows)}

        for future in as_completed(future_to_index):
            i = future_to_index[future]
            title, artist, url = future.result()
            if not title:
                continue
            if url:
                print(f"  → {url}")
                results[i] = url
            else:
                print(f"  → Not found: {artist} - {title}")
                results[i] = f"# NOT FOUND: {artist} - {title}"

    links = [r for r in results if r is not None]

    with open(output_file, "w") as f:
        f.write("\n".join(links))

    print(f"\nDone! {len(links)} links saved to {output_file}")

if __name__ == "__main__":
    playlist_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        base = os.path.splitext(os.path.basename(playlist_file))[0]
        output_file = f"{base}_links.txt"
    playlist_to_youtube_links(playlist_file, output_file)