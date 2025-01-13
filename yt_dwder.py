import yt_dlp
import os
from googleapiclient.discovery import build

# Downloads a YouTube audio from the given URL.
def download_youtube_audio(video_url, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Audio download completed: {video_url}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Downloads a YouTube video from the given URL.
def download_youtube_video(video_url, save_path):
    """
    Downloads a YouTube video from the given URL.

    Args:
        video_url (str): The URL of the YouTube video.
        save_path (str): The folder path where the video will be saved.

    Returns:
        None
    """
    try:
        # Ensure the save directory exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Define yt-dlp options
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Download the best quality video + audio
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Save video with title as filename
            'merge_output_format': 'mp4',  # Merge video and audio into mp4 format
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print(f"Download completed: {video_url}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Classifies the user input as link or artist name.
from urllib.parse import urlparse, parse_qs

def classify_input(user_input):
    """
    Classifies the input as a single video link, a playlist link, or an artist's name.

    Args:
        user_input (str): The input to classify.

    Returns:
        str: The classification of the input.
    """
    try:
        # Parse the input as a URL
        parsed_url = urlparse(user_input)

        # Check if it is a valid URL with a scheme and network location
        if parsed_url.scheme and parsed_url.netloc:
            query_params = parse_qs(parsed_url.query)

            # Check if it's a playlist link
            if "list" in query_params and "v" not in query_params:
                return "Playlist link"
            
            # Check if it's a video link
            if "v" in query_params:
                return "Single video link"
        else:
            # If it's not a valid URL, consider it an artist's name
            return "Artist name"

    except Exception:
        return "Invalid input"

    # If none of the above, consider it an artist's name
    return "Artist name"

# Fetches YouTube links for songs of a given artist or band.
def get_youtube_links(artist_name, api_key, max_results=50):
    """
    Fetches YouTube links for songs of a given artist or band.

    Args:
        artist_name (str): Name of the artist or band.
        api_key (str): YouTube Data API v3 key.
        max_results (int): Maximum number of results to fetch (default: 50).

    Returns:
        list: A list of YouTube video URLs.
    """
    youtube = build("youtube", "v3", developerKey=api_key)

    # Search for videos by the artist
    search_response = youtube.search().list(
        q=artist_name,
        type="video",
        part="id,snippet",
        maxResults=max_results,
        videoCategoryId="10"  # Music category
    ).execute()

    # Extract video IDs and build full URLs
    video_links = []
    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        video_links.append(f"https://www.youtube.com/watch?v={video_id}")

    return video_links

if __name__ == "__main__":
    save_folder = "C:\\Users\\kiree\\Downloads\\yt\\test_webm"
    user_input = input("Enter the YouTube video URL or artist's name: ").strip()
    mp34 = input("Enter 3 for mp3 and 4 for mp4:")
    if classify_input(user_input) == "Single video link" or classify_input(user_input) == "Playlist link":
        video_url = user_input 
        if mp34 == "3":
            download_youtube_audio(video_url, save_folder)
        elif mp34 == "4":
            download_youtube_video(video_url, save_folder)
        else:
            print("Invalid input. Please enter 3 for mp3 or 4 for mp4.")

    else:
        artist = user_input
        API_KEY = "AIzaSyCeLsGVWjjYzYgSmIlgy8amfyGeUC8lqXw"
        links = get_youtube_links(artist, API_KEY)
        Llist = []
        if links:
            print(f"\nYouTube links for {artist}:")
            for link in links:
                print(link)
                Llist.append(link)
                if mp34 == "3":
                    for i in range(len(Llist)):
                        download_youtube_audio(Llist[i], save_folder)
                elif mp34 == "4":
                    for i in range(len(Llist)):
                        download_youtube_video(Llist[i], save_folder)
                else:
                    print("Invalid input. Please enter 3 for mp3 or 4 for mp4.")

        else:
            print(f"No videos found for {artist}.")
