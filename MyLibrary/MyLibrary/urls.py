from django.conf import settings
from django.contrib import admin
from django.urls import path
from Mybooks.views import LoginView, RegisterView, AddBookView, logout_view, book_cover_view, display_book_covers, success
from Mybooks.views import MainView
from django.conf.urls.static import static
from Mybooks.views import BookDetailView
from Mybooks.views import BookDelete
from Mybooks.views import BookSearchView
from Mybooks.views import BookStatusView
from Mybooks.views import BookRateView
from Mybooks.views import BookListView
from Mybooks.views import MyBookListView
from Mybooks.views import MassBookImport
from Mybooks.views import EditBookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', logout_view, name="logout" ),
    path('register', RegisterView.as_view(), name="register"),
    path('addbook', AddBookView.as_view(), name="addbook"),
    path('book/<int:book_id>/', BookDetailView.as_view(), name="book-details"),
    path('book/delete/<int:pk>/', BookDelete.as_view(), name="book-delete"),
    path('book_status/<int:book_id>/', BookStatusView.as_view(), name="book-status"),
    path('book_rate/<int:book_id>/', BookRateView.as_view(), name="book-rate"),
    path('book_search', BookSearchView.as_view(), name="book-search"),
    path('success', success, name='success'),
    path('book_covers', display_book_covers, name='book_covers'),
    path('book_list', BookListView.as_view(), name='book-list'),
    path('my_books', MyBookListView.as_view(), name='my-books'),
    path('mass_import', MassBookImport.as_view(), name='mass-import'),
    path('book_edit/<int:book_id>', EditBookView.as_view(), name='book-edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

