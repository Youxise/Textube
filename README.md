# Textube

This project is a web application that allows users to perform searches within media files (audio or video) transcriptions. The search functionality supports fuzzy matching, stemming, and exact phrase matching.

## Features
- Extract transcriptions from YouTube videos or uploaded media files.
- Store transcriptions and their timestamps in Elasticsearch.
- Perform advanced text search with:
  - Fuzzy matching
  - Stemming and stop word removal
  - Exact phrase matching
- Highlight matching words in search results.

## Technologies Used
- **Backend**: Flask
- **Search Engine**: Elasticsearch
- **Frontend**: HTML, CSS, JavaScript
- **Transcription**: Whisper

## Installation and Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.10
- Elasticsearch
- Flask

### Steps to Run the Project
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/transcription-search-app.git
   cd transcription-search-app
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start Elasticsearch (if not running already).
4. Run the Flask application:
   ```sh
   python app.py
   ```
5. Open your browser and navigate to `http://localhost:5000`.

## API Endpoints
### `POST /process`
- **Description**: Processes a video link or uploaded file and indexes its transcription in Elasticsearch.
- **Parameters**:
  - `videoLink` (string): YouTube video URL (optional)
  - `mp4Upload` (file): Uploaded media file (optional)
  - `sentence` (string): Sentence to search within transcriptions

### `GET /search`
- **Description**: Searches for a sentence in the indexed transcriptions.
- **Parameters**:
  - `query` (string): The search term

## Elasticsearch Indexing
The project uses a custom Elasticsearch index with analyzers:
- `simple_analyzer`: Lowercase only.
- `custom_analyzer`: Lowercase, stopword removal, and stemming.

## Future Improvements
- Migrate the frontend to React for a better user experience.
- Implement a real-time transcription feature.
- Enhance search results with word-level timestamps.

## License
This project is licensed under the **MIT** License.

**Author**: Youxise
