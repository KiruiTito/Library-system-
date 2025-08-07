# Library Management System
# Created by: [Your Name]
# Date: [Date]
# Description: Simple command-line library system for adding, searching, borrowing, and returning books.

import os
import json

# -------------------- Book Class --------------------
class Book:
    def __init__(self, title, author, year, isbn, is_available=True):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.is_available = is_available

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "is_available": self.is_available
        }

    @staticmethod
    def from_dict(data):
        return Book(
            title=data["title"],
            author=data["author"],
            year=data["year"],
            isbn=data["isbn"],
            is_available=data.get("is_available", True)
        )

# -------------------- Global Book List --------------------
library = []

# -------------------- Functions --------------------

def load_books(filename="library_records.txt"):
    if not os.path.exists(filename):
        return
    with open(filename, "r") as file:
        try:
            data = json.load(file)
            for item in data:
                book = Book.from_dict(item)
                library.append(book)
        except json.JSONDecodeError:
            print("Error: Corrupted file format.")

def save_books(filename="library_records.txt"):
    with open(filename, "w") as file:
        data = [book.to_dict() for book in library]
        json.dump(data, file, indent=4)

def add_book():
    print("\nAdd a New Book:")
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year = input("Year Published: ").strip()
    isbn = input("ISBN: ").strip()
    book = Book(title, author, year, isbn)
    library.append(book)
    print(f"Book '{title}' added successfully!")

def display_books():
    if not library:
        print("No books available.")
        return
    print("\nLibrary Collection:")
    for idx, book in enumerate(library, start=1):
        status = "Available" if book.is_available else "Not Available"
        print(f"{idx}. {book.title} by {book.author} | {book.year} | ISBN: {book.isbn} | {status}")

def search_books():
    term = input("Enter title or author to search: ").lower()
    found = [book for book in library if term in book.title.lower() or term in book.author.lower()]
    if not found:
        print("No matching books found.")
        return
    print("\nSearch Results:")
    for book in found:
        status = "Available" if book.is_available else "Not Available"
        print(f"{book.title} by {book.author} | {book.year} | ISBN: {book.isbn} | {status}")

def borrow_book():
    isbn = input("Enter ISBN of the book to borrow: ").strip()
    for book in library:
        if book.isbn == isbn:
            if book.is_available:
                book.is_available = False
                print(f"You have successfully borrowed '{book.title}'.")
                return
            else:
                print("Sorry, that book is already borrowed.")
                return
    print("Book not found.")

def return_book():
    isbn = input("Enter ISBN of the book to return: ").strip()
    for book in library:
        if book.isbn == isbn:
            if not book.is_available:
                book.is_available = True
                print(f"Thank you for returning '{book.title}'.")
                return
            else:
                print("This book wasn't borrowed.")
                return
    print("Book not found.")

def show_menu():
    print("\n====== Library Menu ======")
    print("1. Add Book")
    print("2. Display All Books")
    print("3. Search Book")
    print("4. Borrow Book")
    print("5. Return Book")
    print("6. Exit and Save")
    print("==========================")

# -------------------- Main Program Loop --------------------

def main():
    load_books()
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == '1':
            add_book()
        elif choice == '2':
            display_books()
        elif choice == '3':
            search_books()
        elif choice == '4':
            borrow_book()
        elif choice == '5':
            return_book()
        elif choice == '6':
            save_books()
            print("Library records saved. Exiting...")
            break
        else:
            print("Invalid choice. Please select from 1 to 6.")

if __name__ == "__main__":
    main()
