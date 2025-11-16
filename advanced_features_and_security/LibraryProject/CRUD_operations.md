new_book = Book(title = '1984', author = 'George Orwell',publication_year = 1949)
new_book.save()

Book.objects.all()
#<QuerySet [<Book: 1984 by George Orwell (1949)>]>

existing_book = Book.objects.get(id = 3)
existing_book.title = 'Nineteen Eighty-Four'
existing_book.save()

Book.objects.all()
#<QuerySet [<Book: Nineteen Eighty-Four by George Orwell (1949)>]>

existing_book = Book.objects.get(id = 3)
existing_book.delete()
#(1, {'bookshelf.Book': 1})

Book.objects.all()
#<QuerySet []>