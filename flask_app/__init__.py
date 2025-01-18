from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'its a secret to everybody'

# local database
DATABASE = "wws"
# pythonanywheredatabase
# DATABASE = "jessethommes$wws"

UPLOAD_FOLDER = "flask_app/static/imgs/event_imgs"
# UPLOAD_FOLDER = "/home/jessethommes/Test/flask_app/static/imgs"
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','bmp'}