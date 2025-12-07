Audio Notes Converter API
Project Overview
A Django REST API system for secure document management with user authentication. Users can upload, download, update, and delete their documents (PDF, Word) after authenticating through a JWT-based system.

Project Structure
Audi_Notes_Converter_API/
├── AccountsApp/                # Authentication & User Management
│   ├── models.py               # CustomUser, PasswordResetToken
│   ├── serializers.py          # All authentication serializers
│   ├── views.py                # Authentication views
│   └── urls.py                 # Auth endpoints
├── DocumentsApp/               # Document Management (Coming Week)
│   ├── models.py               # Document model
│   ├── serializers.py          # Document serializers
│   ├── views.py                # CRUD operations
│   └── urls.py                 # Document endpoints
├── Audi_Notes_Converter_API/   # Project settings
│   ├── settings.py             # Main configuration
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI config
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management
└── README.md                   # This file