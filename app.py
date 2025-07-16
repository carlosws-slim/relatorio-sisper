from flask import Flask, request, render_template, Markup
import os
from datetime import datetime
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'arquivo' not in request.files:
            return render_template("index.html", mensagem="Nenhum arquivo enviado.")
        file = request.files['arquivo']
        if file.filename == '':
            return render_template("index.html", mensagem="Nome de arquivo vazio.")
        if file and file.filename.endswith('.xlsx'):
            data_str = datetime.today().strftime('%Y-%m-%d')
            filename = f"{data_str}_{file.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Lê o arquivo Excel com pandas
            try:
                df = pd.read_excel(filepath)
                tabela_html = df.to_html(classes="table table-bordered", index=False, border=0)
                tabela_html = Markup(tabela_html)  # Permite HTML ser renderizado no template
                return render_template("index.html", mensagem="Relatório recebido com sucesso!", tabela=tabela_html)
            except Exception as e:
                return render_template("index.html", mensagem=f"Erro ao ler o Excel: {e}")
        else:
            return render_template("index.html", mensagem="Por favor, envie um arquivo .xlsx válido.")
    return render_template("index.html")
