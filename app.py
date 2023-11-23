from flask import Flask, render_template, request, redirect
import fitz  # PyMuPDF
from gtts import gTTS


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        pdf_text = extract_text_from_pdf(file)

        tts_file_path = text_to_speech(pdf_text)
        tts_file_path= "static\\tts_output.mp3"
        return render_template('result.html', tts_file_path=tts_file_path)

def extract_text_from_pdf(pdf_file):
    text = ''
    pdf_document = fitz.open(stream=pdf_file.read(), filetype='pdf')
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts_file_path = r'D:\SoftwareDevelopment\Projects\pycharm\AudioBook\static\tts_output.mp3'
    tts.save(tts_file_path)
    return tts_file_path


if __name__ == '__main__':
    app.run(debug=True)
