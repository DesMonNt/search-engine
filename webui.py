from flask import Flask, request, render_template, redirect
from utils import Utils
from os import path, startfile
from foogle import Foogle

app = Flask(__name__)
client = Foogle()


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


@app.errorhandler(500)
def internal(e):
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def search():
    keywords, results = [], []
    rank = False
    logic = 'and'

    if not client.documents:
        if request.method == 'POST':
            pass
        return render_template('indexer.html')

    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        rank = 'rank' in request.form
        logic = request.form.get('logic', 'and')

        if query:
            keywords = list(filter(lambda x: len(x) > 0, Utils.split_words(query.lower())))[:40]
            results = client.search(keywords, logic, rank=rank)
            for result in results:
                result.snippet = Utils.highlight_keywords(result.snippet, keywords)

    return render_template('foogle.html', query=' '.join(keywords), results=results, rank=rank, logic=logic)


@app.route('/file/<path:filepath>', methods=['GET'])
def open_file(filepath: str):
    if path.isfile(filepath):
        startfile(filepath)
        return "file is opening"
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
