from flask import Flask, redirect, render_template, request, url_for

import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)

    # TODO
    positives = "positive-words.txt"
    negatives = "negative-words.txt"
    analyzer = Analyzer(positives, negatives)
    positive, negative, neutral = 0, 0, 0
    
    for word in tweets:
        if analyzer.analyze(word) == 1:
            positive = positive + 1
        elif analyzer.analyze(word) == -1:
            negative = negative + 1
        else:
            neutral = neutral + 1

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
