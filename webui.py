from flask import Flask, request, render_template, redirect, jsonify
from utils import Utils
from os import path, startfile
from foogle import Foogle

app = Flask(__name__)
client = None


@app.errorhandler(404)
def page_not_found(_):
    return redirect('/')


@app.errorhandler(500)
def internal(_):
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def search():
    global client

    keywords, results = [], []
    rank = False
    logic = 'and'
    folder_path = str()

    if not client:
        if request.method == 'POST':
            folder_path = request.form.get('path', '').strip()
            if not path.isdir(folder_path):
                return redirect('/')
            client = Foogle(root=folder_path)
            return redirect('/')

        return render_template('indexer.html', path=folder_path)

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
