from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    video = request.files['video']
    if video:
        filepath = os.path.join(UPLOAD_FOLDER, video.filename)
        video.save(filepath)

        # Placeholder AI logic
        processed_path = os.path.join(PROCESSED_FOLDER, "no_watermark_" + video.filename)
        os.system(f"ffmpeg -i {filepath} -vf 'delogo=x=20:y=20:w=100:h=50:show=0' {processed_path}")

        return send_file(processed_path, as_attachment=True)
    return "Upload failed"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)