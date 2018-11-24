import json
from flask import Flask, request

from paraphraser import paraphrase
from tone_analyzer import analyze_tone


app = Flask(__name__)


@app.route('/tone')
def tone():
    text = request.args.get('q')
    tone_analysis = analyze_tone(text)

    return json.dumps(tone_analysis)


@app.route('/noho')
def noho():
    text = request.args.get('q')
    paraphrases = paraphrase(text)

    return json.dumps(paraphrases)
