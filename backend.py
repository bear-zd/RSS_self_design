from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return 'PONG!'


@app.route('/feed/<rssname>', methods=['GET', 'POST'])
def feed(rssname):
    if request.method == 'GET':
        print(fr'feeds/{rssname}.xml')
        with open(fr'feeds/{rssname}.xml', 'r+', encoding='utf-8') as xml:
            content = xml.read()
        return content


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0', port=1234)
