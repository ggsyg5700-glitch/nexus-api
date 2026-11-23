from flask import Flask, request, jsonify
from pytubefix import YouTube
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "NEXUS DOWNLOADER API is Running!"

@app.route('/analyze', methods=['GET'])
def analyze():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    try:
        yt = YouTube(video_url, client='WEB', use_po_token=True)
        
        video_streams = {}
        allowed_heights = ('360p', '480p', '720p', '1080p')

        for stream in yt.streams.filter(file_extension='mp4', only_video=True):
            if stream.video_codec and 'avc1' in stream.video_codec:
                if stream.resolution in allowed_heights:
                    video_streams[stream.resolution] = stream.url

        best_audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
        best_audio = best_audio_stream.url if best_audio_stream else None

        return jsonify({
            "status": "success",
            "title": yt.title,
            "thumbnail": yt.thumbnail_url,
            "videos": video_streams,
            "best_audio": best_audio
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
