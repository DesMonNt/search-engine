import multiprocessing
import tkinter as tk
from os import path, startfile
from tkinter import filedialog

from flask import Flask, jsonify, redirect, render_template, request

from foogle import Foogle
from utils import Utils

app = Flask(__name__)

with open(path.join('config', 'encodings'), 'r') as file:
    encodings = ['auto'] + file.read().split()
client: Foogle | None = None


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
            folder_path = request.form.get('folderPath', '')
            encoding = request.form.get('encoding', 'auto').strip()
            if not path.exists(folder_path):
                return redirect('/')
            client = Foogle(root=folder_path, encoding=encoding)
            return redirect('/')

        return render_template('indexer.html', path=folder_path, dropdown_list=encodings)

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
    if path.isfile(filepath) and client and Utils.is_file_in_folder(filepath, client.root):
        startfile(filepath)
        return "file is opening"
    return redirect('/')


def open_folder_dialog(queue: multiprocessing.Queue):
    window = tk.Tk()
    window.withdraw()
    queue.put(filedialog.askdirectory())
    window.destroy()


@app.route('/select-folder', methods=['GET'])
def select_folder():
    if client:
        return redirect('/')

    queue = multiprocessing.Queue()

    tkinter_process = multiprocessing.Process(target=open_folder_dialog, args=(queue,))
    tkinter_process.start()
    tkinter_process.join()
    tkinter_process.terminate()

    return jsonify({'path': queue.get()})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
