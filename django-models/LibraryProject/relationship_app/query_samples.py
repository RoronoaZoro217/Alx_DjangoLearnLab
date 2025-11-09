
author = Author.objects.get(name="Author Name")
books = author.books.all()

books = Book.objects.filter(author__name="Author Name")


books = Book.objects.filter(author_id=1)


library = Library.objects.get(name="Library Name")
books = library.books.all()

books = Book.objects.filter(libraries__name="Library Name")

books = Book.objects.filter(libraries__id=1)


library = Library.objects.get(name="Library Name")
librarian = library.librarian

librarian = Librarian.objects.get(library__name="Library Name")

librarian = Librarian.objects.get(library_id=1)