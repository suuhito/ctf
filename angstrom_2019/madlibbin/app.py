import binascii

import os
import re

from flask import Flask
from flask import request
from flask import redirect, render_template

app = Flask(__name__)
app.secret_key = 'flag'

data = {}


def generate():
    return binascii.hexlify(os.urandom(16)).decode()


def parse(x):
    return list(dict.fromkeys(
        re.findall(r'(?<=\{args\[)[\w\-\s]+(?=\]\})', x)))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def create():
    tag = generate()
    template = request.form.get('template', '')
    madlib = {
        'template': template,
        'blanks': parse(template)
    }
    data[tag] = madlib
    return redirect('/{}'.format(tag))


@app.route('/<tag>', methods=['GET'])
def view(tag):
    if tag != 'favicon.ico':
        madlib = data[tag]
        if set(request.args.keys()) == set(madlib['blanks']):
            print(dir(request.args.__init__.__globals__))
            # print(request.args)
            # print(madlib['template'].format(args=request.args))
            return render_template('result.html', stuff=madlib['template'].format(args=request.args))
        else:
            return render_template('fill.html', blanks=madlib['blanks'])


if __name__ == '__main__':
    app.run()
