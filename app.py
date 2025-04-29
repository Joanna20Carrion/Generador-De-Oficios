from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
import io
import zipfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    excel_file = request.files["excel"]
    word_file = request.files["word"]
    pdf_transmision = request.files.get("pdf_transmision")
    pdf_generacion = request.files.get("pdf_generacion")
    pdf_distribucion = request.files.get("pdf_distribucion")
    pdf_cliente_libre = request.files.get("pdf_cliente_libre")
    codigos_input = request.form.get("codigos")

    pdf_files = {
        "Transmisión": pdf_transmision,
        "Generación": pdf_generacion,
        "Distribución": pdf_distribucion,
        "Cliente Libre": pdf_cliente_libre
    }

    codigos = [codigo.strip() for codigo in codigos_input.split(",")]

    try:
        df = pd.read_excel(excel_file, header=0, engine="openpyxl")
        print("Columnas encontradas:", df.columns.tolist())
    except Exception as e:
        return jsonify({"error": f"Error al leer el archivo Excel: {str(e)}"})

    print("Columnas cargadas desde el Excel:", df.columns)
    df.columns = df.columns.str.strip()
    print("Columnas después de la limpieza:", df.columns)

    if "CODIGO" not in df.columns:
        return jsonify({"error": "La columna 'CODIGO' no existe en el archivo Excel. Verifique los nombres de las columnas."})

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for codigo in codigos:
            fila = df[df["CODIGO"] == codigo]

            if fila.empty:
                print(f"Código {codigo} no encontrado en el Excel.")
                continue

            nombre_destinatario = fila["GERENTE GENERAL"].values[0]
            cargo = fila["CARGO DEL REPRESENTANTE"].values[0]
            entidad = fila["RAZON SOCIAL"].values[0]
            direccion = fila["DIRECCIÓN"].values[0]
            distrito = fila["Distrito"].values[0]
            actividad = fila["ACTIVIDAD"].values[0]  # Tipo de actividad: Generación, Transmisión, etc.

            documento = Document(word_file)
            
            print(f"Valor de entidad antes del reemplazo: {entidad}")

            for parrafo in documento.paragraphs:
                for run in parrafo.runs:
                    if "[Nombre del Destinatario]" in run.text:
                        run.text = run.text.replace("[Nombre del Destinatario]", nombre_destinatario)
                        run.font.bold = True
                        run.font.name = "Poppins"
                        run.font.size = Pt(9.5)
                    if "[Cargo]" in run.text:
                        run.text = run.text.replace("[Cargo]", cargo)
                        run.font.name = "Poppins"
                        run.font.size = Pt(9.5)
                    if "[Entidad]" in run.text:
                        nuevo_texto = run.text.replace("[Entidad]", str(entidad))
                        run.clear() 
                        run.add_text(nuevo_texto) 
                        run.font.bold = True
                        run.font.name = "Poppins"
                        run.font.size = Pt(9.5)
                    if "[Dirección]" in run.text:
                        run.text = run.text.replace("[Dirección]", direccion)
                        run.font.name = "Poppins"
                        run.font.size = Pt(9.5)
                    if "[Distrito]" in run.text:
                        run.text = run.text.replace("[Distrito]", distrito)
                        run.font.underline = True
                        run.font.name = "Poppins"
                        run.font.size = Pt(9.5)

            doc_buffer = io.BytesIO()
            documento.save(doc_buffer)
            doc_buffer.seek(0)
            
            # Define el nombre del documento y la ruta dentro del ZIP
            nombre_documento = f"OFICIO-{entidad.replace(' ', '_')}.docx"
            ruta_carpeta_empresa = f"{actividad}/{codigo}/{nombre_documento}"
            zip_file.writestr(ruta_carpeta_empresa, doc_buffer.read())

            # Agrega los PDFs a la carpeta correspondiente
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
