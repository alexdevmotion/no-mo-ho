import json
from flask import Flask, request
from paraphraser import paraphrase

app = Flask(__name__)


@app.route('/noho')
def noho():
    text = request.args.get('q')
    paraphrases = paraphrase(text)

    return json.dumps(paraphrases)

