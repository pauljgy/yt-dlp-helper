## Dependencies: python, yt-dlp, deno

This is a small utility for taking a playlist in apple music, and converting it to mp3s for use in DJ software/production.

Usage:

1. In Apple Music, go to File > Library > Export Playlist, and export the playlist info as a .txt file, which we can call "Playlist.txt" for now. Export as UTF-16.

2. Run "python applemusic_to_yt.py 'Playlist.txt'" to get a new .txt file, with each line containing a youtube link for each song in the original playlist. The output will be called "Playlist_output_links.txt".

3. Run "python links_to_mp3.py 'Playlist_output_links.txt'" to actually execute the download process for the songs.

4. The downloaded songs will be stored in a root directory folder called "batch".

Notes:
- You can add youtube/soundcloud links however you like to the "*_output_links.txt" file. Good for snagging whichever extra edit/VIP that might only be in some random YT/SC link with double-digit plays.
- Currently uses up to 5 threads for converting playlist into YT links, and up to 3 threads for the actual download execution.

Future:
- Claude can probably one-shot making this Spotify compatible. Just need to figure out how Spotify exports playlists to .txt files.