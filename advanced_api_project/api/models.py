from django.db import models
from datetime import datetime

# Create your models here.
# This model represents an author who can write multiple books.
# It establishes the "one" side of a one-to-many relationship with the Book model.
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# This model represents a book written by an author.
# It establishes the "many" side of a one-to-many relationship with the Author model.
# Multiple books can be associated with a single author.
class Book(models.Model):
    title = models.CharField(max_length=300)
    publication_year = models.IntegerField()
    
    # Foreign key establishes the relationship between Book and Author
    # on_delete=models.CASCADE ensures that when an author is deleted,
    # all their associated books are also deleted (cascade delete)
    # related_name='books' allows reverse lookup from Author to Books
    # (i.e., author.books.all() will return all books by that author)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        # String representation showing book title and author
        return f"{self.title} by {self.author.name}"

    class Meta:
        # Order books by publication year (newest first)
        ordering = ['-publication_year']