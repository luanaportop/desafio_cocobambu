from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


API_KEY = 'AIzaSyA67We01EHCBmWjBObUQLS5OpjxjJYq1Dk'

# Variáveis para armazenar favoritos e anotações
favorite_books = []
book_notes = {}
book_ratings = {}

# Função para buscar livros da API 
def get_books(query="python"):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])  
    return []

# Rota principal para exibir livros e gerenciar favoritos
@app.route('/')
def index():
    query = request.args.get('q', '')  
    books = get_books(query=query)
    return render_template('index.html', books=books, favorites=favorite_books, notes=book_notes, ratings=book_ratings)

# Rota para adicionar um livro aos favoritos
@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    book_title = request.form.get('title')
    if book_title and book_title not in favorite_books:
        favorite_books.append(book_title)
    return redirect(url_for('index'))

# Rota para adicionar anotações e avaliações
@app.route('/add_note_rating', methods=['POST'])
def add_note_rating():
    book_title = request.form.get('title')
    note = request.form.get('note')
    rating = request.form.get('rating')

    if book_title:
        book_notes[book_title] = note
        book_ratings[book_title] = rating
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


