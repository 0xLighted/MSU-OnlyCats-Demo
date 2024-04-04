from flask import Flask, render_template
from subprocess import Popen

app = Flask(__name__)
DEBUG = True


@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    if DEBUG:
        Popen('npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch', shell=True)
    app.run(host='0.0.0.0', port=80, debug=DEBUG)
