from flask import Flask, request, send_file, render_template
from pytubefix import YouTube
from moviepy.editor import AudioFileClip
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "URL is required", 400

    try:
        # 유튜브 비디오 다운로드
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(filename='audio.mp4')

        # mp4 파일을 mp3로 변환
        audio_clip = AudioFileClip('audio.mp4')
        audio_clip.write_audiofile('audio.mp3')
        audio_clip.close()

        # mp4 파일 삭제
        os.remove('audio.mp4')

        return send_file('audio.mp3', as_attachment=True, download_name='audio.mp3')
    except Exception as e:
        # 예외 발생 시 디버깅 정보 출력
        print(f"Error: {e}")
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)