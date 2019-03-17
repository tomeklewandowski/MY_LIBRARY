from django.db import models
from django.contrib.auth.models import User


genre_lit = (
    (1, "Fantasy"),
    (2, "Westerns"),
    (3, "Romance"),
    (4, "Thriller"),
    (5, "Criminal"),
    (6, "Biography"),
    (7, "Children's books"),
    (8, "Non-fiction"),
    (9, "Sci-fi"),
    (10, "Novels")
)

genre_rate = (
    ("1", "No way"),
    ("2", "Weak"),
    ("3", "Nearly"),
    ("4", "Interesting"),
    ("5", "Good"),
    ("6", "Very good"),
    ("7", "I can't tear myself away"),
    ("8", "Masterpiece"),
)

book_stat = (
    (1, "To read"),
    (2, "In progress"),
    (3, "Done"),
)


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    literary_genre = models.SmallIntegerField(choices=genre_lit, default=None)
    isbn = models.CharField(max_length=17, unique=True)
    publisher = models.CharField(max_length=200)
    synopsis = models.CharField(max_length=9000, default=None)
    book_cover = models.ImageField(upload_to='media/covers/', null=True)
    rate = models.ManyToManyField(User, through="BookRate")

    @property
    def name(self):
        return "{}".format(self.title)

    def __str__(self):
        return self.title


# class User(models.Model):
#     first_name = models.CharField(max_length=64)
#     last_name = models.CharField(max_length=64)
#     email = models.EmailField(unique=True)
#     user_name = models.CharField(max_length=30, unique=True)
#
#     @property
#     def name(self):
#         return "{}".format(self.user_name)
#
#     def __str__(self):
#         return self.user_name


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    own_books = models.ManyToManyField(Book, related_name="book")


class Review(models.Model):
    content = models.TextField(max_length=5000)
    creation_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BookComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=2000, null=True)


class BookRate(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.FloatField(choices=genre_rate, default=None)


class BookStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=book_stat, default=None)

