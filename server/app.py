import uuid
import sys, os

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
# sys.path.append(os.path.dirname(os.path.join(os.path.abspath(__file__), '../')))
from modules.processes import *

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__, template_folder=os.path.abspath('src/templates'))
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def hello():
    hello = "Hello world"
    return hello


@app.route('/', methods=['GET'])
def top():
    return render_template('top.html')

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