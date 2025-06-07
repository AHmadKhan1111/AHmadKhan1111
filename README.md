# YouTube Video Downloader

A simple Python script to download YouTube videos.

## Features

- Downloads the highest resolution progressive stream available.
- Shows download progress.
- Basic error handling for invalid URLs and unavailable videos.
- Command-line interface.

## Prerequisites

- Python 3.x
- `pytube` library

## Installation

1.  **Clone the repository (or download the script):**
    ```bash
    # If it were a git repo:
    # git clone <repository_url>
    # cd youtube-downloader
    ```
    For now, just ensure you have `youtube_downloader.py`.

2.  **Install dependencies:**
    Open your terminal or command prompt and run:
    ```bash
    pip install pytube
    ```

## Usage

1.  Run the script from your terminal:
    ```bash
    python youtube_downloader.py
    ```
2.  When prompted, enter the full YouTube video URL and press Enter.
3.  The video will be downloaded to the same directory where the script is located.

## Example

```bash
python youtube_downloader.py
Enter the YouTube video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Fetching video information for 'Rick Astley - Never Gonna Give You Up (Official Music Video)'...
Starting download for 'Rick Astley - Never Gonna Give You Up (Official Music Video)' (Size: XX.XX MB)...
Downloading: 100.00% completed (XX.XXMB / XX.XXMB)
'Rick Astley - Never Gonna Give You Up (Official Music Video)' downloaded successfully to '.'!
```
*(Note: Actual size and progress display may vary slightly based on the script's output format)*

## TODO (Future Enhancements)

- Allow specifying output directory via command-line argument.
- Allow choosing video resolution/format.
- Batch downloading from a list of URLs.
- GUI version.
