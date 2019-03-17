
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, AddBookForm, BookSearchForm, BookStatusForm
from django.views import View
from .models import Book, BookStatus
from django.views.generic import DeleteView
# from ebooklib import epub
#
# book = epub.read_epub('test.epub')


class MainView(View):
    def get(self, request):
        ctx = {"book": Book}
        return render(request, "base.html", ctx)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
                #return HttpResponse(f'Welcome {username}')
            else:
                return HttpResponse("Ups, You are not log in.")


def logout_view(request):
    logout(request)
    return redirect('/')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            ctx = {"user": user}
            return render(request, "new_user.html", ctx)


class MassAddBookView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('ha')


class AddBookView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddBookForm()
        return render(request, "addbook.html", {"form": form})

    def post(self, request):
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            literary_genre = form.cleaned_data.get('literary_genre')
            isbn = form.cleaned_data.get('isbn')
            publisher = form.cleaned_data.get('publisher')
            synopsis = form.cleaned_data.get('synopsis')
            book_cover = form.cleaned_data.get('book_cover')
            book = Book(title=title,
                        author=author,
                        literary_genre=literary_genre,
                        isbn=isbn, publisher=publisher,
                        synopsis=synopsis,
                        book_cover=book_cover)
            try:
                book.save()
            except IntegrityError:
                return HttpResponse('This book is already here.')
            ctx = {"book": book}
            return render(request, "new_book.html", ctx)
        else:
            return render(request, "addbook.html", {"form": form})


class BookDetailView(View):

    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        ctx = {"book": book}
        return render(request, "new_book.html", ctx)


class BookDelete(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = '/'


class BookSearchView(View):
    def get(self, request):
        form = BookSearchForm()
        return render(request, "book_search.html", {"form": form})

    def post(self, request):
        form = BookSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            books = Book.objects.filter(title__icontains=search)
            return render(request, "book.html", {"books": books})


def book_cover_view(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = AddBookForm()
    return render(request, 'add_cover_book.html', {'form': form})


def success(request):
    return HttpResponse('successfuly uploaded')


def display_book_covers(request):
    if request.method == 'GET':
        Books = Book.objects.all()
        return render((request, 'display_book_covers.html',
                       {'book_covers': Books}))


class BookStatusView(View):
    def get(self, request, book_id):
        book = Book.objects.get(id=book_id)
        form = BookStatusForm(initial={"Book":  f'{book.title} by {book.author}'})
        return render(request, "book_status.html", {"form": form, "book":  book})

    def post(self, request, book_id):
        form = BookStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data.get('status')
            book = Book.objects.get(id=book_id)
            BookStatus.objects.create(book=book, status=status)
            return HttpResponse("Success")
