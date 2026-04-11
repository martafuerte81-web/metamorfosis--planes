from flask import Flask, request, jsonify, send_file
import json, os, tempfile, traceback
from generar_plan_pdf import generar_pdf

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'status': 'ok', 'servicio': 'Metamorfosis — Generador de Planes PDF'})

@app.route('/generar', methods=['POST'])
def generar():
    try:
        datos = request.get_json(force=True)
        if not datos:
            return jsonify({'error': 'No se recibieron datos'}), 400

        # Generar PDF en archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            output_path = tmp.name

        generar_pdf(datos, output_path)

        nombre = datos.get('nombre', 'Cliente').replace(' ', '_')
        filename = f'Plan_Metamorfosis_{nombre}.pdf'

        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
