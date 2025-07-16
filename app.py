import os
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Nenhum arquivo foi enviado.'
    file = request.files['file']
    if file.filename == '':
        return 'Nenhum arquivo selecionado.'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            df = pd.read_excel(filepath)
            preview_html = df.head().to_html(classes="table table-striped", index=False)
            return render_template("preview.html", preview_html=preview_html)
        except Exception as e:
            return f"Erro ao processar o arquivo: {str(e)}"

    return 'Tipo de arquivo não permitido.'

if __name__ == '__main__':
    app.run(debug=True)
