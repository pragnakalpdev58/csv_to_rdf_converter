import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/pragnakalp-l-12/Desktop/upload'
ALLOWED_EXTENSIONS = {'.ttl'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def nothing():
    print('''Nothing to see here. Everything works on api "/api/upload"''')

@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': f'File {filename} uploaded successfully'})
    else:
        return jsonify({'error': 'Invalid file format'})

if __name__ == "__main__":
    app.run(port=5000)
