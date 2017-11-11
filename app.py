from flask import Flask, render_template
import json
from random import randint
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/random',methods=['POST'])
def random_number():
    print "WHAT"
    response = {
        'randomNumber': randint(1, 100)
    }
    return json.dumps(response)

if __name__ == '__main__':
    app.run()