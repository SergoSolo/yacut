from flask import abort, render_template

from . import app


@app.route('/')
def index_view():
    return render_template('index.html')
    