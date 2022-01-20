from flask import Flask, request, render_template, Response, jsonify, send_file
from crypto import hex_digest_sha256, generate_keys, decipherECB
from io import BytesIO

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/sha256')
def sha256():
    return render_template('sha256.html')


@app.route('/RSA')
def RSA():
    return render_template('RSA.html')


@app.route('/decipher')
def decipher():
    return render_template('decipher.html')


@app.route('/digest/sha256', methods=['POST'])
def digest_sha256():
    if 'file' not in request.files:
        return Response('No file part', status=400)

    file = request.files['file']
    if not file:
        return Response('No selected file', status=400)

    bytes_file = file.read()
    hex_digest = hex_digest_sha256(bytes_file)

    return jsonify(digest=hex_digest)


@app.route('/key/rsa', methods=['POST'])
def key_rsa():
    size = int(request.form['size'])
    if size not in [1024, 2048]:
        return Response(status=400)

    public_key, private_key = generate_keys(size)

    formatted_private = private_key.replace('\n', '<br />')
    formatted_public = public_key.replace('\n', '<br />')

    return jsonify(private=formatted_private, public=formatted_public)


@app.route('/decipher/link', methods=['POST'])
def decipher_link():
    link = request.form['link']
    password = request.form['password']

    try:
        filename, data = decipherECB(link, password)
        buffer = BytesIO(data)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
        )
    except Exception as e:
        return Response(str(e), status=400)


if __name__ == '__main__':
    app.run()
