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

            # Processar o arquivo depois do upload
            resumo = processar_relatorio(filepath)
            return f"Relatório recebido com sucesso!<br><br>{resumo}"
        else:
            return "Por favor, envie um arquivo .xlsx válido."
    return render_template("index.html")

def processar_relatorio(caminho):
    try:
        df = pd.read_excel(caminho, skiprows=1)
        df = df.dropna(how='all')  # remove linhas totalmente vazias
        if 'DATA' not in df.columns or 'ATENDIDO POR - MÉDICO' not in df.columns:
            return "Arquivo enviado não possui colunas esperadas."

        df_today = df[df['DATA'] == pd.to_datetime(datetime.today().date())]
        total = len(df_today)

        resumo = f"Total de atendimentos hoje: <strong>{total}</strong><br>"
        if total > 0:
            por_medico = df_today['ATENDIDO POR - MÉDICO'].value_counts()
            for medico, qtde in por_medico.items():
                resumo += f"- {medico}: {qtde} paciente(s)<br>"
        return resumo
    except Exception as e:
        return f"Erro ao processar o relatório: {str(e)}"

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
