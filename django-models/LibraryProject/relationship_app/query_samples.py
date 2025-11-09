
author = Author.objects.get(name="Author Name")
books = author.books.all()

library_name = "Library Name" 
library = Library.objects.get(name=library_name)
books = library.books.all()


library = Library.objects.get(name="Library Name")
librarian = library.librarian

librarian = Librarian.objects.get(library__name="Library Name")

librarian = Librarian.objects.get(library_id=1)