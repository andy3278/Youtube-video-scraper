import os
import json
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Replace with your own API key
API_KEY = 'YOUR_API_KEY'

def search_videos(keyword, max_results=10):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    search_response = youtube.search().list(
        q=keyword,
        part='id,snippet',
        maxResults=max_results,
        type='video'
    ).execute()

    video_ids = [item['id']['videoId'] for item in search_response['items']]
    video_titles = [item['snippet']['title'] for item in search_response['items']]

    return zip(video_ids, video_titles)

def get_transcripts(video_ids):
    transcripts = []
    for video_id in video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcripts.append(transcript)
        except:
            transcripts.append(None)

    return transcripts

def main():
    keyword = input("Enter a keyword to search for videos: ")
    videos = search_videos(keyword)

    output_data = []

    for video_id, title in videos:
        video_data = {"title": title}

        transcript = get_transcripts([video_id])[0]
        if transcript is not None:
            video_data["transcript"] = transcript
        else:
            video_data["transcript"] = "Transcript not available"

        output_data.append(video_data)

    with open('output.json', 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

if __name__ == '__main__':
    main()
