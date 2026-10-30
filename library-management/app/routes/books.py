from flask import Blueprint, jsonify, request, render_template, redirect, url_for

from app import store
from app.models.book import Book

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("", methods=["GET"])
def list_books():
    results = list(store.books.values())
    search = request.args.get("search", "").lower()
    if search:
        results = [b for b in results if search in b.title.lower() or search in b.author.lower()]
    return jsonify([b.to_dict() for b in results])


@books_bp.route("", methods=["POST"])
def create_book():
    data = request.get_json()
    book_id = store.next_id("book")
    book = Book(
        id=book_id,
        title=data["title"],
        author=data["author"],
        genre=data["genre"],
        isbn=data["isbn"],
        total_copies=data.get("total_copies", 1),
        available_copies=data.get("total_copies", 1),
    )
    store.books[book_id] = book
    return jsonify(book.to_dict()), 201


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = store.books.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict())


@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = store.books.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    data = request.get_json()
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.genre = data.get("genre", book.genre)
    book.isbn = data.get("isbn", book.isbn)
    book.total_copies = data.get("total_copies", book.total_copies)
    book.available_copies = data.get("available_copies", book.available_copies)
    return jsonify(book.to_dict())


@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = store.books.pop(book_id, None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return "", 204



# Edit book

@books_bp.route("/<int:book_id>", methods=["PUT", "POST"])
def change_book(book_id):
    book = store.books.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.isbn = data.get("isbn", book.isbn)
    book.genre = data.get("genre", book.genre)
    
    if "total_copies" in data:
        book.total_copies = int(data.get("total_copies"))

    if request.is_json:
        return jsonify(book.to_dict()), 200
    else:
        return redirect(url_for("views.books_page")) 



@books_bp.route("/<int:book_id>/edit", methods=["GET"])
def edit_book_page(book_id):
    book = store.books.get(book_id)
    if book is None:
        return "Book not found", 404
    return render_template("edit_book.html", book=book)


