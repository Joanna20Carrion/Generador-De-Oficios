from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
from docx import Document
from docx.shared import Pt
import io
import zipfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_razones_sociales", methods=["POST"])
def get_razones_sociales():
    excel_file = request.files["excel"]
    try:
        df = pd.read_excel(excel_file, sheet_name="General", engine="openpyxl")
        razones = df["RAZON SOCIAL"].dropna().unique().tolist()
        return jsonify({"razones": razones})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/generate", methods=["POST"])
def generate():
    excel_file = request.files["excel"]
    word_file = request.files["word"]
    pdf_transmision = request.files.get("pdf_transmision")
    pdf_generacion = request.files.get("pdf_generacion")
    pdf_distribucion = request.files.get("pdf_distribucion")
    pdf_cliente_libre = request.files.get("pdf_cliente_libre")
    razones_input = request.form.getlist("razones")

    pdf_files = {
        "Transmisión": pdf_transmision,
        "Generación": pdf_generacion,
        "Distribución": pdf_distribucion,
        "Cliente Libre": pdf_cliente_libre
    }

    try:
        df = pd.read_excel(excel_file, engine="openpyxl")
        df.columns = df.columns.str.strip()
    except Exception as e:
        return jsonify({"error": f"Error al leer el archivo Excel: {str(e)}"})

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for razon in razones_input:
            fila = df[df["RAZON SOCIAL"] == razon]

            if fila.empty:
                print(f"Razón Social {razon} no encontrada.")
                continue

            nombre_destinatario = fila["GERENTE GENERAL"].values[0]
            cargo = fila["CARGO DEL REPRESENTANTE"].values[0]
            entidad = fila["RAZON SOCIAL"].values[0]
            direccion = fila["DIRECCIÓN"].values[0]
            distrito = fila["Distrito"].values[0]
            actividad = fila["ACTIVIDAD"].values[0]
            codigo = fila["CODIGO"].values[0]

            documento = Document(word_file)

            for parrafo in documento.paragraphs:
                for run in parrafo.runs:
                    if "[Nombre del Destinatario]" in run.text:
                        run.text = run.text.replace("[Nombre del Destinatario]", nombre_destinatario)
                        run.font.bold = True
                        run.font.name = "Poppins"
                        run.font.size = Pt(9)
                    if "[Cargo]" in run.text:
                        run.text = run.text.replace("[Cargo]", cargo)
                        run.font.name = "Poppins"
                        run.font.size = Pt(9)
                    if "[Entidad]" in run.text:
                        nuevo_texto = run.text.replace("[Entidad]", str(entidad))
                        run.clear()
                        run.add_text(nuevo_texto)
                        run.font.bold = True
                        run.font.name = "Poppins"
                        run.font.size = Pt(9)
                    if "[Dirección]" in run.text:
                        run.text = run.text.replace("[Dirección]", direccion)
                        run.font.name = "Poppins"
                        run.font.size = Pt(9)
                    if "[Distrito]" in run.text:
                        run.text = run.text.replace("[Distrito]", distrito)
                        run.font.underline = True
                        run.font.name = "Poppins"
                        run.font.size = Pt(9)

            doc_buffer = io.BytesIO()
            documento.save(doc_buffer)
            doc_buffer.seek(0)

            nombre_documento = f"OFICIO-{entidad.replace(' ', '_')}.docx"
            ruta_carpeta_empresa = f"{actividad}/{codigo}/{nombre_documento}"
            zip_file.writestr(ruta_carpeta_empresa, doc_buffer.read())

            pdf_file = pdf_files.get(actividad)
            if pdf_file:
                pdf_name = pdf_file.filename or f"{actividad}.pdf"
                pdf_file.stream.seek(0)
                pdf_bytes = pdf_file.stream.read()
                ruta_pdf = f"{actividad}/{codigo}/{pdf_name}"
                zip_file.writestr(ruta_pdf, pdf_bytes)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name="oficios_generados.zip",
        mimetype="application/zip"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
