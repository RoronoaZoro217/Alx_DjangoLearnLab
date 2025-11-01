existing_book = Book.objects.get(id = 3)
existing_book.delete()
#(1, {'bookshelf.Book': 1})

Book.objects.all()
#<QuerySet []>