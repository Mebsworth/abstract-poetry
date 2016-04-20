import os
from flask import render_template, flash, redirect, send_from_directory, request, url_for
from app import app
from forms import ImageUploadForm
from werkzeug import secure_filename
from clarifai.client import ClarifaiApi
from nlg.poem_generator import PoemGenerator 
from nlg.chain_builder import ChainBuilder

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
clarifai_api = ClarifaiApi()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def convert_to_ascii(words):
    for i in range(0,len(words)):
        words[i] = words[i].decode('utf-8')
    return words

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')


@app.route('/view/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    #response = send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)
    path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    result = clarifai_api.tag_images(open(path, 'rb'))
    tags = result['results'][0]['result']['tag']['classes']
    tags = convert_to_ascii(tags)
    #tags = ["painting", "art", "graffiti", "spray","vandalism", "artistic", "mural", "airbrush", "wall", "creativity", "illustration", "signature", "color", "messy", "print", "color", "art", "motley", "canvas", "design"]
    cb = ChainBuilder()
    cb.build_chain()
    chain = cb.get_chain()
    pg = PoemGenerator(tags, chain)
    poem = pg.get_poem()
    #poem = convert_to_ascii(poem)
    print(poem)
    filepath = "http://127.0.0.1:5000/uploads/" + filename
    return render_template('view.html', filepath=filepath, tags=tags, poem=poem)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)
