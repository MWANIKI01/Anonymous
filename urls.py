from flask import Blueprint, url_map, url_for, render_template, send_from_directory, send_static, direct
from flask.staticfiles import send_file
import os

bp = Blueprint('static', __name__)

@bp.app.route('/static/<path:re(.*)$>')
def serve_static(path):
    return send_from_directory(app.config['STATIC_FOLDER'], path)

@bp.app.route('/static/<path:filename>')
@bp.app.route('/static/<filename>')
@app.route('/static/<filename>')
@bp.route('/static/<path:filename>.<ext>')
def send_static_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

@bp.app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(bp)