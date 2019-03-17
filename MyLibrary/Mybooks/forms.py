from django import forms
from django.core.validators import EmailValidator
from .models import Book, BookStatus, BookRate, BookComments
from django.forms import ModelForm


class LoginForm (forms.Form):
    username = forms.CharField(label="Login", strip=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class UserDataForm(forms.Form):
    first_name = forms.CharField(label="Name", max_length=100)
    last_name = forms.CharField(label="Surname", max_length=100)
    email = forms.CharField(label="mail", max_length=100, validators=[EmailValidator()])


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, strip=True, label="Please enter your login")
    password = forms.CharField(label="Enter password", widget=forms.PasswordInput)
    password_again = forms.CharField(label="Password again", widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=50, strip=True, label="Enter your name")
    last_name = forms.CharField(max_length=50, strip=True, label="Enter your surname")
    email = forms.EmailField(max_length=50, label="Enter your email")

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")

        if password != password_again:
            raise forms.ValidationError(
                "password and password_again does not match")


class AddBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'author', 'literary_genre', 'isbn', 'publisher', 'synopsis', 'book_cover']


class BookSearchForm(forms.Form):
    search = forms.CharField(max_length=100, strip=True, label="Search", help_text="Title needed")


class BookStatusForm(forms.Form):

    class Meta:
        model = BookStatus
        fields = '__all__'


class BookRateForm(forms.Form):

    class Meta:
        model = BookRate
        fields = '__all__'


class BookCommentsForm(forms.Form):

    class Meta:
        model = BookComments
        fields = '__all__'



