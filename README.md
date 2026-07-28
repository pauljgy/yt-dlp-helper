## Dependencies: python, yt-dlp, deno

This is a small utility for downloading mp3s from a .txt file of YouTube/SoundCloud links, for use in DJ software/production.

Usage:

1. Create a .txt file with one link per line (e.g. `links.txt`).

2. Run `python convert.py links.txt` to download the audio for each link.

3. The downloaded songs will be saved to the `Recently Downloaded/` folder.

Notes:
- Lines starting with `#` are skipped, so you can comment out links.
- Currently uses up to 4 threads for the download process.
