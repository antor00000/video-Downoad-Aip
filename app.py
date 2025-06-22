from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        video_url = data['url']

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        formats = []
        for f in info.get('formats', []):
            if f.get('url') and f.get('ext') == 'mp4' and f.get('acodec') != 'none':
                formats.append({
                    'format': f"{f.get('format_note', 'unknown')} - {f.get('height')}p",
                    'url': f['url']
                })

        return jsonify({
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'links': formats[:5]
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
