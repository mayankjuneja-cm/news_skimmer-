from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for

from google_news import NewsOfIntreast


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("main.html")

@app.route("/do_search")
def do_search():
    term = request.args.get('search')
    loc = request.args.get('loc', "AE")

    if not loc:
        loc = "AE"

    news_sites = request.args.getlist('hello')

    term = term + " " + " ".join(news_sites)

    return redirect(url_for('search', loc=loc, topic=term))

@app.route("/<loc>/<topic>")
def search(loc, topic):
    loc = loc.upper()
    noi = NewsOfIntreast(topic, loc, datetime.today() - timedelta(days=1))

    grouping = noi.group
    return render_template("home.html", grouping=grouping)


if __name__ == "__main__":
    app.run(debug=True)