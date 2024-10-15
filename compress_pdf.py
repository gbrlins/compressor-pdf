from flask import Flask, request, jsonify, send_file, render_template
import fitz  # PyMuPDF
from PIL import Image
import io
import datetime
import os
import logging
import tempfile

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

def compress_pdf(input_path, output_path, compress_factor=1.2):
    logging.info(f'Iniciando a compressão do PDF: {input_path}')
    doc = None  # Inicializando como None
    try:
        doc = fitz.open(input_path)

        for page_number in range(len(doc)):
            page = doc.load_page(page_number)

            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)

                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))

                # Calcular novo tamanho mantendo a proporção
                new_width = int(image.width / compress_factor)
                new_height = int(image.height / compress_factor)
                resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                img_buffer = io.BytesIO()
                resized_image.save(img_buffer, format="JPEG", quality=85)  # Mudando para JPEG com qualidade ajustável
                img_buffer.seek(0)

                # Insere a imagem redimensionada na página
                page.insert_image(page.rect, stream=img_buffer.read())

        doc.save(output_path)
        logging.info(f'PDF comprimido salvo em: {output_path}')
    except Exception as e:
        logging.error(f'Erro ao comprimir o PDF: {e}')
        raise  # Relançar a exceção para tratar no endpoint
    finally:
        if doc is not None:
            doc.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_endpoint():
    pdf_file = request.files['file']
    compress_factor = float(request.form.get('compress_factor', 1.2))

    # Usar um arquivo temporário para evitar conflitos
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_input:
        input_path = temp_input.name
        pdf_file.save(input_path)

        # Obtém o nome do arquivo original sem a extensão
        original_filename = os.path.splitext(pdf_file.filename)[0]

        # Cria o timestamp com data e dia da semana
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%A')  # Formato: AAAAMMDD_DIA
        output_path = f"{original_filename}_{timestamp}.pdf"  # Nome do arquivo de saída

        try:
            compress_pdf(input_path, output_path, compress_factor)
            logging.info(f'Arquivo comprimido com sucesso: {output_path}')
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            logging.error(f'Erro na compressão: {e}')
            return jsonify({"error": "Erro ao comprimir o PDF."}), 500
        finally:
            os.remove(input_path)  # Limpar o arquivo temporário
            if os.path.exists(output_path):
                os.remove(output_path)  # Limpar o arquivo comprimido se for necessário

# O bloco abaixo não será usado quando o Gunicorn é executado
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8080)
