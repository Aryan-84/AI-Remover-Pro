from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename

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
    if 'video' not in request.files:
        return 'No video uploaded', 400

    video = request.files['video']
    if video.filename == '':
        return 'No selected video', 400

    filename = secure_filename(video.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_filename = "no_watermark_" + filename
    output_path = os.path.join(PROCESSED_FOLDER, output_filename)

    video.save(input_path)

    # FFmpeg watermark removal using delogo filter
    os.system(f"ffmpeg -y -i {input_path} -vf \"delogo=x=20:y=20:w=100:h=50:show=0\" {output_path}")

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
