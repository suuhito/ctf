"""
配布されているアプリにsearch.pyを組み合わせたもの
os.environが見つかるとprintするようにしている
"""

import binascii

import os
import re

from flask import Flask
from flask import request
from flask import redirect, render_template

app = Flask(__name__)
app.secret_key = os.environ.get('FLAG')

data = {}


def search(obj, max_depth):

    visited_clss = []
    visited_objs = []

    def visit(obj, path='obj', depth=0):
        yield path, obj

        if depth == max_depth:
            return

        elif isinstance(obj, (int, float, bool, str, bytes)):
            return

        elif isinstance(obj, type):
            if obj in visited_clss:
                return
            visited_clss.append(obj)

        else:
            if obj in visited_objs:
                return
            visited_objs.append(obj)

        # attributes
        for name in dir(obj):
            if name.startswith('__') and name.endswith('__'):
                if name not in ('__globals__', '__class__', '__self__',
                                '__weakref__', '__objclass__', '__module__'):
                    continue
            attr = getattr(obj, name)
            if name == 'environ':
                # os.environがあればprint
                print(path)
            yield from visit(attr, '{}.{}'.format(path, name), depth + 1)

        # dict values
        if hasattr(obj, 'items') and callable(obj.items):
            try:
                for k, v in obj.items():
                    yield from visit(v, '{}[{}]'.format(path, repr(k)), depth)
            except:
                pass

        # items
        elif isinstance(obj, (set, list, tuple, frozenset)):
            for i, v in enumerate(obj):
                yield from visit(v, '{}[{}]'.format(path, repr(i)), depth)

    yield from visit(obj)


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
            # 探索の深さを指定
            for i in search(request.args, 5):
                pass
            return render_template('result.html', stuff=madlib['template'].format(args=request.args))
        else:
            return render_template('fill.html', blanks=madlib['blanks'])


if __name__ == '__main__':
    app.run()
