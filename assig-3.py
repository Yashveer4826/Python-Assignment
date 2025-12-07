class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"


import json
import logging
from pathlib import Path
from .book import Book

logging.basicConfig(level=logging.INFO, filename="library.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class LibraryInventory:
    def __init__(self, file_path="catalog.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_catalog()

    def load_catalog(self):
        try:
            if self.file_path.exists():
                data = json.loads(self.file_path.read_text())
                self.books = [Book(**book_data) for book_data in data]
                logging.info("Catalog loaded successfully.")
            else:
                logging.warning("Catalog file not found. Starting new.")
                self.books = []
        except Exception as e:
            logging.error(f"Error loading catalog: {e}")
            self.books = []

    def save_catalog(self):
        try:
            data = [book.to_dict() for book in self.books]
            self.file_path.write_text(json.dumps(data, indent=4))
            logging.info("Catalog saved.")
        except Exception as e:
            logging.error(f"Error saving catalog: {e}")

    
    def add_book(self, book: Book):
        self.books.append(book)
        self.save_catalog()

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return self.books


from library_manager.book import Book
from library_manager.inventory import LibraryInventory

def menu():
    print("\n===== LIBRARY INVENTORY MANAGER =====")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")

def main():
    inventory = LibraryInventory()

    while True:
        menu()
        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")
                inventory.add_book(Book(title, author, isbn))
                print("Book added!")

            elif choice == "2":
                isbn = input("Enter ISBN to issue: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.issue():
                    inventory.save_catalog()
                    print("Book issued.")
                else:
                    print("Cannot issue (maybe already issued).")

            elif choice == "3":
                isbn = input("Enter ISBN to return: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.return_book():
                    inventory.save_catalog()
                    print("Book returned.")
                else:
                    print("Cannot return (maybe already available).")

            elif choice == "4":
                books = inventory.display_all()
                if books:
                    for b in books:
                        print(b)
                else:
                    print("No books in library.")

            elif choice == "5":
                title = input("Enter title keyword: ")
                results = inventory.search_by_title(title)
                for b in results:
                    print(b)

            elif choice == "6":
                print("Exiting...")
                break

            else:
                print("Invalid choice!")

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()