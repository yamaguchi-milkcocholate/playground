import uuid
import sys, os

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from modules.processes import *

# configuration
DEBUG = True

# instantiate the app
app = Flask(
    __name__,
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../dist/static')),
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../dist')),
    )
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route('/api/mnist', methods=['POST'])
def mnist():
    response_object = {'status': 'success'}
    data = request.get_json()
    img_str, width, height = data['img'], data['width'], data['height']
    img = ParameterParser.to_numpy(img_str)

    dig_cls = DigitClassifier()
    img_pro = ImageProcessor(gray_x=img, width=width, height=height)

    response_object['data'] = list()
    for result in img_pro.divide_to_digit():
        response_object['data'].append({
            'prediction': dig_cls.predict(x=result['input']),
            'img_str': result['raw_digit'],
            'width': result['width'],
            'height': result['height'],
        })
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()