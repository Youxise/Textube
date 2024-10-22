from yt_dlp import YoutubeDL
import os

def download_youtube_video(UPLOAD_FOLDER, video_link):
    # Download YouTube video using yt-dlp
    ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': f'{UPLOAD_FOLDER}/%(title)s.%(ext)s'
            }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_link, download=True)
        media_file = os.path.join(UPLOAD_FOLDER, f"{info['title']}.{info['ext']}")

    return media_file

# Function to transcribe media file directly with Whisper
def transcribe_media(model, media_path):
    # Transcribe the media file using Whisper's small model
    result = model.transcribe(media_path)

    # Get the full transcription
    transcription = result['text']

    # We don't have word-level timestamps in the small model, so we approximate segments
    duration = result['segments'][-1]['end'] if result['segments'] else 0
    segment_length = 30  # 30 seconds per segment

    segments = []
    for i in range(0, int(duration // segment_length) + 1):
        start_time = i * segment_length
        end_time = min((i + 1) * segment_length, duration)
        segments.append({
            'text': transcription,
            'start': start_time,
            'end': end_time
        })

    return transcription, segments


