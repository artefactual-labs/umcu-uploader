from flask import Flask
from flask import render_template
from flask import url_for


app = Flask(__name__)
# # urls for each of the static pages
# style = url_for('static', filename='styles.css')
# root_page = url_for('templates', filename='index.html')

@app.route("/")
def root():
    # render template can be passed  variables in the context.
    return render_template('index.html')
