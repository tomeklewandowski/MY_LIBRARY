from django.conf import settings
from django.contrib import admin
from django.urls import path
from Mybooks.views import LoginView, RegisterView, AddBookView, logout_view, book_cover_view, display_book_covers, success
from Mybooks.views import MainView
from django.conf.urls.static import static
from django.contrib.auth import views
from Mybooks.views import BookDetailView
from Mybooks.views import BookDelete
from Mybooks.views import BookSearchView
from Mybooks.views import BookStatusView

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
    path('book_search', BookSearchView.as_view(), name="book-search"),
    path('success', success, name='success'),
    path('book_covers', display_book_covers, name='book_covers'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

