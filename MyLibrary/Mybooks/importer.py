from pyepub import EPUB
from os import walk
import hashlib
from Mybooks.models import Book


def extract_isbn(epub):
    if epub.id == "Aspose" or epub.id.startswith('http'):
        return hashlib.md5(epub.title.encode("utf-8")).hexdigest()
    else:
        return epub.id


def process(file):
    epub = EPUB(file)
    print(f'Title: {epub.title}, Author: {epub.author}, ISBN: {extract_isbn(epub)}')
    book = Book(title=epub.title,
                author=epub.author,
                isbn=extract_isbn(epub))
    book.save()


def epub_import(path):
    for root, dirs, files in walk(path):
        for file in files:
            if file.endswith('.epub'):
                try:
                    process(root+'/'+file)
                except Exception as err:
                    print(err)
