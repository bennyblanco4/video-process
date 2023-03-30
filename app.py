from flask import Flask, render_template, request, send_from_directory
from moviepy.editor import *
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    video = request.files['video']
    start_time = int(request.form['start_time'])
    video.save(os.path.join(app.config['UPLOAD_FOLDER'], video.filename))

    cut_video(video.filename, start_time)

    return send_from_directory(app.config['OUTPUT_FOLDER'], f'cut_{video.filename}', as_attachment=True)

def cut_video(filename, start_time):
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'cut_{filename}')

    video = VideoFileClip(input_path)
    cut_video = video.subclip(start_time)
    cut_video.write_videofile(output_path)

    os.remove(input_path)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('output'):
        os.makedirs('output')
    app.run(debug=True)
