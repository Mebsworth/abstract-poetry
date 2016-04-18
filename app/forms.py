from flask.ext.wtf import Form
from wtforms import FileField
from wtforms.validators import DataRequired

class ImageUploadForm(Form):
    image = FileField('Upload image')

