from flask import Flask, request, render_template
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
            return "Nenhum arquivo enviado."
        file = request.files['arquivo']
        if file.filename == '':
            return "Nome de arquivo vazio."
        if file and file.filename.endswith('.xlsx'):
            data_str = datetime.today().strftime('%Y-%m-%d')
            filename = f"{data_str}_{file.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Lê a planilha
            df = pd.read_excel(filepath)

            # Converte para HTML e exibe na nova página
            table_html = df.to_html(classes="table table-striped", index=False)
            return render_template("preview.html", table=table_html)
        else:
            return "Por favor, envie um arquivo .xlsx válido."
    return render_template("index.html")

# Roda localmente ou no Render
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
