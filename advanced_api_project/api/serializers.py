from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# This serializer handles the conversion of Book model instances to/from JSON.
# It includes custom validation to ensure data integrity.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # Serialize all fields of the Book model
        fields = ['id', 'title', 'publication_year', 'author']
    
    # Custom validation for publication_year field
    # This method ensures that the publication year is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        return value

# This serializer handles the conversion of Author model instances to/from JSON.
# It includes a nested BookSerializer to serialize related books dynamically.
# This demonstrates a one-to-many relationship serialization.
class AuthorSerializer(serializers.ModelSerializer):
    # The 'books' field uses the related_name defined in the Book model's ForeignKey
    # many=True indicates this is a one-to-many relationship
    # read_only=True means books can be read but not created/updated through this serializer
    # This provides a nested representation of all books by this author
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']