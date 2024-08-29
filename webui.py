from threading import Thread
from webbrowser import open
from flask import Flask, request, render_template
from foogle import Foogle

app = Flask(__name__)
foogle = Foogle()


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

    return render_template('foogle.html', query=query, results=results, rank=rank, logic=logic)


if __name__ == "__main__":
    browser_thread = Thread(target=open("http://127.0.0.1:5000/"))
    browser_thread.start()

    app.run(debug=False, use_reloader=False)
