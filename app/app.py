import os
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from static.helpers import allowed_file
from static import algo

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = {'jpg', 'png'} 


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename, extensions=ALLOWED_EXTENSIONS):
      filename = secure_filename(file.filename)
      og_img = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(og_img)
      path = f'./images/{filename}'
      output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'labeled_image.png')
      algo.cclabeling(path, output_path)
      return redirect(url_for('labeling', filename=filename))
  return render_template("index.html")

@app.route('/labeling')
def labeling():
  filename = request.args.get('filename')
  return render_template("labeler.html", filename=filename)


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename)
