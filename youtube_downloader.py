"""
YouTube Video Downloader

This script allows you to download YouTube videos in the highest available progressive resolution.

Usage:
    python youtube_downloader.py

The script will then prompt you to enter the YouTube video URL.
Downloaded videos will be saved in the same directory where the script is run,
unless an output path is explicitly specified in the code (currently defaults to script directory).
"""
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable, PytubeError
# It's good practice to also consider requests.exceptions if pytube doesn't wrap them all
# For now, we'll rely on PytubeError or general Exception for network issues not caught by pytube.
# from requests.exceptions import ConnectionError # Example if direct handling is needed

def get_video_url():
    """Prompts the user to enter a YouTube video URL and returns it."""
    url = input("Enter the YouTube video URL: ")
    return url

def download_video(url, output_path='.'):
    """
    Downloads a YouTube video from the given URL with progress and error handling.
    """
    try:
        yt = YouTube(url)

        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage_of_completion = bytes_downloaded / total_size * 100
            downloaded_mb = bytes_downloaded / (1024 * 1024)
            total_mb = total_size / (1024 * 1024)
            print(f"Downloading: {percentage_of_completion:.2f}% completed ({downloaded_mb:.2f}MB / {total_mb:.2f}MB)", end='\r')

        yt.register_on_progress_callback(on_progress)

        # Fetch title first to use in messages
        video_title = yt.title
        print(f"Fetching video information for: '{video_title}'...")

        stream = yt.streams.filter(progressive=True).get_highest_resolution()

        if stream:
            filesize_mb = stream.filesize / (1024 * 1024) if stream.filesize else 0
            size_display = f"{filesize_mb:.2f} MB" if filesize_mb > 0 else "Unknown size"
            print(f"Starting download for '{video_title}' (Size: {size_display})...")
            stream.download(output_path)
            # Ensure the success message is on a new line after progress indicator
            print(f"\n'{video_title}' downloaded successfully to '{output_path}'!")
        else:
            # Ensure message is on a new line if on_progress was called (even if no stream found after title fetch)
            print(f"\nNo suitable progressive stream found for '{video_title}'.")

    except RegexMatchError:
        print(f"\nError: Invalid YouTube URL format entered: '{url}'")
    except VideoUnavailable:
        # Attempt to get video title for a more user-friendly message if possible, otherwise use URL
        title_info = "the video"
        try:
            title_info = f"video '{yt.title}'"
        except: # If yt object or title is not available at this point
            title_info = f"video at '{url}'"
        print(f"\nError: {title_info} is unavailable. It may be private, deleted, or region restricted.")
    except PytubeError as e:
        print(f"\nA Pytube library error occurred: {e}")
    # except ConnectionError: # Import from requests.exceptions if specific handling is desired
    #     print("\nError: Network connection problem. Please check your internet connection.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

def main():
    """
    Main function to handle user input and initiate download.
    """
    video_url = get_video_url()
    if video_url:
        # (Optional) Get output path from user input
        # output_path = input("Enter the download directory (leave blank for current directory): ") or "."
        # download_video(video_url, output_path) # If using custom output path
        download_video(video_url) # Downloads to current directory by default
    else:
        print("No URL entered. Exiting.")

if __name__ == "__main__":
    main()
