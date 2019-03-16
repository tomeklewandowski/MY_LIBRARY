from django.conf import settings
from django.contrib import admin
from django.urls import path
from Mybooks.views import LoginView, RegisterView, AddBookView, logout_view, book_cover_view, display_book_covers, success
from Mybooks.views import MainView
from django.conf.urls.static import static
from django.contrib.auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', logout_view, name="logout" ),
    path('register', RegisterView.as_view(), name="register"),
    path('addbook', AddBookView.as_view(), name="addbook"),
    path('image_upload', book_cover_view, name='image_upload'),
    path('success', success, name='success'),
    path('book_covers', display_book_covers, name = 'book_covers'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

