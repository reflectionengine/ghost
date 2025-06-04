from flask import Flask, render_template, request, redirect, url_for
from rag_logic import load_documents, generate_report

app = Flask(__name__)
vector_store = load_documents()


@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    if request.method == 'POST':
        query = request.form.get('query', '')
        reflection = bool(request.form.get('reflection'))
        if query:
            passages = vector_store.search(query)
            report = generate_report(query, passages, reflection=reflection)
    return render_template('index.html', report=report)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('document')
    if file and file.filename:
        text = file.read().decode('utf-8', errors='ignore')
        vector_store.add_document(text)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
