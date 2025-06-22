from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forceurl': True,
        'forcejson': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            download_links = [
                {
                    "format": f"{f.get('format_note', 'Unknown')} - {f.get('ext')}",
                    "url": f.get("url"),
                    "filesize": f.get("filesize", 0)
                }
                for f in formats if f.get("url")
            ]
            return jsonify({
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "links": download_links
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "✅ Video Download API is Live!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)