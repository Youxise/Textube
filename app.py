import os
import whisper
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from elasticsearch import Elasticsearch

from search import search_transcriptions, index_transcription, create_index_with_analyzers
from transcription import download_youtube_video, transcribe_media

app = Flask(__name__)

# Folder where media files will be temporarily saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize models
model = whisper.load_model("small")
es = Elasticsearch("http://localhost:9200")
index_name = "transcriptions"

@app.route('/')
def home():
    return render_template('index.html')

# Route to handle video/audio processing
@app.route('/process', methods=['POST'])
def process_video():

    video_link = request.form.get('videoLink')
    uploaded_file = request.files.get('mp4Upload')
    sentence = request.form.get('sentence')

    if not sentence:
        return jsonify({'status': 'error', 'message': 'Please provide a sentence to search for.'}), 400

    media_file = None

    # Process YouTube link
    if video_link:
        try:
            media_file = download_youtube_video(UPLOAD_FOLDER, video_link)
        except Exception:
            return jsonify({'status': 'error', 'message': 'Error downloading media link'}), 500

    # Process uploaded media file (MP4, MP3, MKV, etc.)
    elif uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        media_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #uploaded_file.save(media_file)
    else:
        return jsonify({'status': 'error', 'message': 'Error uploading media file'}), 400

    if media_file:
        # Transcribe the media file
        transcription, segments = transcribe_media(model, media_file)
        print("transcriptions : \n", transcription)
        print("\nsegments : \n", segments)

        # Index the transcription and segments in ElasticSearch
        index_transcription(es, index_name, segments)

        # Search for the sentence in the transcriptions
        results = search_transcriptions(es, index_name, sentence)
        print("\nresults : \n", results)

        # Render the index.html template and pass the results
        return render_template('index.html', results=results)

    return jsonify({'status': 'error', 'message': 'No media file or link provided.'}), 400


if __name__ == '__main__':
    # Create the index with analyzers (run this once)
    create_index_with_analyzers(es, index_name)
    es.indices.get(index=index_name)

    # Run the Flask app
    app.run(debug=True)
