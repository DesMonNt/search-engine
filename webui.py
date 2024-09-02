from threading import Thread
from webbrowser import open
from flask import Flask, request, render_template, redirect, url_for
import re
from os import path, startfile
from foogle import Foogle

app = Flask(__name__)
foogle = Foogle()


def highlight_keywords(text, keywords):
    for word in keywords:
        pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
        text = pattern.sub(f'<span class="highlight">{word}</span>', text)

    return text


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


@app.errorhandler(500)
def internal(e):
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def search():
    query = ""
    results = []
    rank = False
    logic = 'and'

    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        rank = 'rank' in request.form
        logic = request.form.get('logic', 'and')

        if query:
            if logic == 'and':
                results = foogle.search(query, rank=rank)
            elif logic == 'or':
                results = foogle.search_or(query, rank=rank)

            keywords = query.split()

            for result in results:
                result.snippet = highlight_keywords(result.snippet, keywords)

    return render_template('foogle.html', query=query, results=results, rank=rank, logic=logic)


@app.route('/file/<path:filepath>', methods=['GET'])
def open_file(filepath: str):
    if path.isfile(filepath):
        startfile(filepath)
        return "file is opening"
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
