from flask import Flask, request, jsonify
import yt_dlp
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

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])

            video_streams = {}
            best_audio = None
            best_audio_abr = 0
            allowed_heights = [360, 480, 720, 1080]

            for f in formats:
                vcodec = f.get('vcodec', 'none')
                acodec = f.get('acodec', 'none')
                ext = f.get('ext', '')
                url = f.get('url')

                if vcodec != 'none' and 'avc1' in vcodec and ext == 'mp4' and url:
                    height = f.get('height')
                    if height in allowed_heights:
                        label = f"{height}p"
                        video_streams[label] = url

                if vcodec == 'none' and acodec != 'none' and ext == 'm4a' and url:
                    abr = f.get('abr') or 0
                    if abr > best_audio_abr:
                        best_audio_abr = abr
                        best_audio = url

            return jsonify({
                "status": "success",
                "title": info.get('title', 'Video'),
                "thumbnail": info.get('thumbnail', ''),
                "videos": video_streams,
                "best_audio": best_audio
            })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
