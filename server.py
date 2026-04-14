from flask import Flask, request, send_file, jsonify
from careeros_report_generator_v2 import build_report
import tempfile
import os

app = Flask(__name__)

@app.route('/generate-report', methods=['POST'])
def generate():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            tmp_path = f.name

        build_report(data, tmp_path)
        return send_file(
            tmp_path,
            mimetype='application/pdf',
            download_name='PB-CareerOS-Pro-Report.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'careeros-pdf-generator'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
