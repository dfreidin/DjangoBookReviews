# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
import bcrypt

# Create your views here.
def index(request):
    r_form = RegistrationForm()
    l_form = LoginForm()
    context = {
        "r_form": r_form,
        "l_form": l_form
    }
    return render(request, "book_reviews/index.html", context)

def books(request):
    if not "user_id" in request.session:
        return redirect(index)
    user = User.objects.get(id=request.session["user_id"])
    recent_reviews = Review.objects.order_by("-created_at")[:3]
    other_books = list(Book.objects.all())
    for r in recent_reviews:
        if r.book in other_books:
            other_books.remove(r.book)
    context = {
        "user": user,
        "reviews": recent_reviews,
        "books": other_books
    }
    return render(request, "book_reviews/books.html", context)

def add(request):
    if not "user_id" in request.session:
        return redirect(index)
    user = User.objects.get(id=request.session["user_id"])
    b_form = BookForm()
    r_form = ReviewForm
    context = {
        "user": user,
        "b_form": b_form,
        "r_form": r_form
    }
    return render(request, "book_reviews/add.html", context)

def show_book(request, id):
    if not "user_id" in request.session:
        return redirect(index)
    user = User.objects.get(id=request.session["user_id"])
    books = Book.objects.filter(id=id)
    form = ReviewForm()
    if len(books) < 0:
        return redirect(books)
    context = {
        "user": user,
        "book": books[0],
        "form": form
    }
    return render(request, "book_reviews/show_book.html", context)

def show_user(request, id):
    if not "user_id" in request.session:
        return redirect(index)
    users = User.objects.filter(id=id)
    if len(users) < 1:
        return redirect(books)
    num_revs = len(users[0].reviews.all())
    context = {
        "user": users[0],
        "num_revs": num_revs
    }
    return render(request, "book_reviews/show_user.html", context)

def register(request):
    if request.method != "POST":
        return redirect(books)
    form = RegistrationForm(request.POST)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.password = bcrypt.hashpw(form.cleaned_data["password"].encode(), bcrypt.gensalt())
        new_user.save()
        request.session["user_id"] = new_user.id
        return redirect(books)
    return redirect(index)

def login(request):
    if request.method != "POST":
        return redirect(books)
    form = LoginForm(request.POST)
    if form.is_valid():
        users = User.objects.filter(email=form.cleaned_data["email"])
        if len(users) < 1:
            messages.error(request, "Email or password is incorrect")
            return redirect(index)
        user = users[0]
        pw = form.cleaned_data["password"]
        if bcrypt.checkpw(pw.encode(), user.password.encode()):
            request.session["user_id"] = user.id
            return redirect(books)
    return redirect(index)

def logout(request):
    request.session.flush()
    return redirect(index)

def add_book(request):
    if not "user_id" in request.session:
        return redirect(index)
    if request.method != "POST":
        return redirect(books)
    b_form = BookForm(request.POST)
    r_form = ReviewForm(request.POST)
    user = User.objects.get(id=request.session["user_id"])
    if all([b_form.is_valid(), r_form.is_valid()]):
        new_book = b_form.save()
        new_review = r_form.save(commit=False)
        new_review.book = new_book
        new_review.reviewer = user
        new_review.save()
        return redirect(show_book, id=new_book.id)
    return redirect(books)

def add_review(request, id):
    if not "user_id" in request.session:
        return redirect(index)
    if request.method != "POST":
        return redirect(books)
    form = ReviewForm(request.POST)
    books = Book.objects.filter(id=id)
    if len(books) < 1:
        return redirect(books)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.book = books[0]
        new_review.reviewer = User.objects.get(id=request.session["user_id"])
        new_review.save()
        return redirect(show_book, id=id)
    return redirect(books)
    
def delete_review(request, id):
    if not "user_id" in request.session:
        return redirect(index)
    reviews = Review.objects.filter(id=id)
    user = User.objects.get(id=request.session["user_id"])
    if len(reviews) > 0 and reviews[0].reviewer == user:
        book = reviews[0].book
        reviews[0].delete()
        return redirect(show_book, id=book.id)
    return redirect(show_book, id=reviews[0].book.id)