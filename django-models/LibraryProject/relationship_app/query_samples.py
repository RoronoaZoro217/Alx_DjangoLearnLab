author_name = "Ledger"
author = Author.objects.get(name=author_name)
books = Book.objects.filter(author=author)

library_name = "Library Name" 
library = Library.objects.get(name=library_name)
books = library.books.all()

librarian = Librarian.objects.get(library=library)