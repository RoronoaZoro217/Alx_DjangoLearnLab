existing_book = Book.objects.get(id = 3)
existing_book.title = 'Nineteen Eighty-Four'
existing_book.save()
Book.objects.all()
#<QuerySet [<Book: Nineteen Eighty-Four by George Orwell (1949)>]>