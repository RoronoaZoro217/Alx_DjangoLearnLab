from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

# Only users with 'can_view' permission can see the list of books
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
