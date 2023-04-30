from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import sqlite3
from werkzeug.utils import secure_filename
from lstm_utils import get_essay_score, preprocess_essay

# Create folders for storing uploaded files
UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'json', 'xml'}

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a SQLite database for storing marking history
def init_db():
    conn = sqlite3.connect('marking_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (
                author_name TEXT, 
                essay TEXT, 
                score REAL
             )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['author_name']
        essay = request.form['essay']
        essay_file = request.files.get('essay_file', None)
        prompt = request.form['prompt']
        rubric_file = request.files['rubric']
        peer_marks = request.form['peer_marks'].split(',')

        if essay_file and allowed_file(essay_file.filename):
            filename = secure_filename(essay_file.filename)
            essay_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'essays', filename)
            essay_file.save(essay_filepath)
            with open(essay_filepath, 'r') as file:
                essay = file.read()

        if rubric_file and allowed_file(rubric_file.filename):
            filename = secure_filename(rubric_file.filename)
            rubric_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'rubrics', filename)
            rubric_file.save(rubric_filepath)

        # Process the essay using the marking rubric and the machine learning model
        # Replace the get_essay_score function with your actual processing logic
        score = get_essay_score(essay)

        conn = sqlite3.connect('marking_history.db')
        c = conn.cursor()
        c.execute("INSERT INTO history (author_name, essay, score) VALUES (?, ?, ?)", (name, essay, score))
        conn.commit()
        conn.close()
        return jsonify({'score': score})

    return render_template('index.html')


@app.route('/history', methods=['GET'])
def history():

    conn = sqlite3.connect('marking_history.db')
    c = conn.cursor()
    c.row_factory = sqlite3.Row
    c.execute("SELECT * FROM history")
    rows = c.fetchall()
    conn.close()

    return render_template('history.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)


       
