from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, AddBookForm, BookSearchForm, BookStatusForm, BookRateForm
from django.views import View
from .models import Book, BookStatus, BookRate
from django.views.generic import DeleteView
from . import importer


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
                return render(request, 'info.html', {'text': 'Congratulations. You are logged in.', 'url': '/'})
            else:
                return render(request, 'info.html', {'text': 'Sorry. Login failed.', 'url': '/login'})


def logout_view(request):
    logout(request)
    return render(request, 'info.html', {'text': 'You are logged out.', 'url': '/'})


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
        query = BookStatus.objects.filter(user=request.user).filter(book=book)
        if query.exists():
            status = query.first()
        else:
            status = ''
        query = BookRate.objects.filter(book=book)
        if query.exists():
            rate = query.all()
            rate_list = list(rate)
        else:
            rate_list = []
        ctx = {"book": book, "status": status, "rates": rate_list}
        return render(request, "new_book.html", ctx)


class BookDelete(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = '/'


class BookSearchView(View):
    def get(self, request):
        form = BookSearchForm(request.GET)
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
        return render(request, 'display_book_covers.html',
                       {'book_covers': Books})


class BookStatusView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        book = Book.objects.get(id=book_id)
        form = BookStatusForm()
        return render(request, "book_status.html", {"form": form, "book":  book})

    def post(self, request, book_id):
        form = BookStatusForm(request.POST)
        if form.is_valid():
            book = Book.objects.get(id=book_id)
            user = request.user
            query = BookStatus.objects.filter(user=user).filter(book=book)
            status = form.cleaned_data.get('status')
            if query.exists():
                query.update(status=status)
            else:
                BookStatus.objects.create(status=status, book=book, user=user)
            return redirect("/book/"+str(book_id))


class BookRateView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        book = Book.objects.get(id=book_id)
        form = BookRateForm()
        return render(request, "book_rate.html", {"form": form, "book":  book})

    def post(self, request, book_id):
        form = BookRateForm(request.POST)
        if form.is_valid():
            book = Book.objects.get(id=book_id)
            user = request.user
            query = BookRate.objects.filter(user=user).filter(book=book)
            rate = form.cleaned_data.get('rate')
            comment = form.cleaned_data.get('comment')
            if query.exists():
                query.update(rate=rate, comment=comment)
            else:
                BookRate.objects.create(rate=rate, comment=comment, book=book, user=user)
            return redirect("/book/" + str(book_id))


class BookListView(LoginRequiredMixin, View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, "book_list.html", {"books": books})


class MyBookListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        my_books = BookStatus.objects.filter(user=user)
        return render(request, "my_books_list.html", {"books": my_books})


class MassBookImport(LoginRequiredMixin, View):
    def get(self, request):
        importer.epub_import('/home/tomek/Dokumenty/TL_ebook/klasyka500')
        return render(request, 'info.html', {'text': 'Congratulations. Import done.', 'url': '/'})


class EditBookView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        form = AddBookForm(instance=Book.objects.get(id=book_id))
        return render(request, "editbook.html", {"form": form, "book_id": book_id})

    def post(self, request, book_id):
        form = AddBookForm(request.POST, request.FILES, instance=Book.objects.get(id=book_id))
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                return HttpResponse('This book is already here.')
            return redirect("/book/"+str(book_id))
        else:
            return render(request, "addbook.html", {"form": form})




