import os
from flask import render_template, flash, redirect, send_from_directory, request, url_for
from app import app
from forms import ImageUploadForm
from werkzeug import secure_filename
from clarifai.client import ClarifaiApi
from nlg.poem_generator import PoemGenerator 
from nlg.chain_builder import ChainBuilder
import random

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
dumb_tags = ['artistic', 'art', 'painting', 'canvas', 'illustration', 'print', 'abstract']
clarifai_api = ClarifaiApi()
tags = None
chain = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def convert_to_ascii(words):
    for i in range(0,len(words)):
        words[i] = words[i].decode('utf-8')
    return words

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    global chain
    if chain is None:
        cb = ChainBuilder()
        cb.build_chain()
        chain = cb.get_chain()
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global tags
    tags = None
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            return redirect(url_for('view_uploaded_file', filename=filename))
    return render_template('upload.html')


@app.route('/view/<filename>', methods=['GET', 'POST'])
def view_uploaded_file(filename):
    #tags = ["painting", "art", "graffiti", "spray","vandalism", "artistic", "mural", "airbrush", "wall", "creativity", "illustration", "signature", "color", "messy", "print", "color", "art", "motley", "canvas", "design"]
    tags = get_tags(filename)
    for d in dumb_tags:
        if d in tags:
            tags.remove(d)
    poem = get_poem(tags, chain)
    #poem = convert_to_ascii(poem)
    print(poem)
    filepath = "http://127.0.0.1:5000/uploads/" + filename
    return render_template('view.html', filepath=filepath, tags=tags, poem=poem, filename=filename)

def get_tags(filename):
    global tags
    if tags is None:
        path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        result = clarifai_api.tag_images(open(path, 'rb'))
        tags = result['results'][0]['result']['tag']['classes']
        tags = convert_to_ascii(tags)
    return tags

def get_poem(tags, chain):
    pg = PoemGenerator(tags, chain)
    full_poem = pg.get_poem()
    new_poem = full_poem
    if len(full_poem) > 3:
        poem_length = int(random.uniform(3,len(full_poem)))
        new_poem = []
        for i in range(0,poem_length):
            line_idx = int(random.uniform(0,len(full_poem)))
            new_poem.append(full_poem[line_idx])
            del full_poem[line_idx]
    # get rid of final comma
    last_line = new_poem[len(new_poem)-1]
    last_char = last_line[len(last_line)-1]
    if last_char == ',' or last_char == ';' or last_char == ':':
        last_line = last_line[:-1]
        new_poem[len(new_poem)-1] = last_line
    return new_poem


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)
