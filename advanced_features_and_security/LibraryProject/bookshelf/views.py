from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from .forms import ExampleForm

# Only users with 'can_view' permission can see the list of books
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()  # Django ORM automatically parameterizes queries, safe from SQL injection
    return render(request, 'bookshelf/book_list.html', {'books': books})


# Only users with 'can_create' permission can add a new book
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():  # form.is_valid() ensures input is validated and sanitized
            form.save()  # ORM handles safe insertion into the database
            return redirect('book_list')
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})
