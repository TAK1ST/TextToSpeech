from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
from googletrans import Translator
import pykakasi
import io

app = Flask(__name__)
kakasi = pykakasi.kakasi()  # Khởi tạo pykakasi để chuyển đổi Kanji sang Hiragana
translator = Translator()   # Khởi tạo dịch vụ dịch thuật

# Trang chính
@app.route('/')
def index():
    return render_template('index.html')

# Xử lý văn bản và chuyển đổi sang Hiragana, dịch sang tiếng Việt
@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    # Chuyển đổi sang Hiragana
    result = kakasi.convert(text)
    hiragana = ' '.join([item['hira'] for item in result])
    # Dịch sang tiếng Việt
    translation = translator.translate(text, src='ja', dest='vi')
    return jsonify({'original': text, 'hiragana': hiragana, 'translation': translation.text})

# Chuyển văn bản thành giọng nói
@app.route('/tts', methods=['POST'])
def tts():
    text = request.form['text']
    lang = request.form['lang']
    tts = gTTS(text=text[2:], lang=lang)
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    return send_file(audio_io, mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(debug=True)