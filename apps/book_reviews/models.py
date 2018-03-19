# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    content = models.TextField()
    RATING_CHOICES = ((1,1),(2,2),(3,3),(4,4),(5,5))
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book, related_name="reviews")
    reviewer = models.ForeignKey(User, related_name="reviews")

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            "name",
            "alias",
            "email",
            "password"
        ]
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        pw = cleaned_data.get("password")
        pc = cleaned_data.get("confirm_password")
        if pw != pc:
            raise forms.ValidationError("Password does not match")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "author"
        ]

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.RadioSelect(
        choices=Review.RATING_CHOICES,
        attrs={"class": "form-check form-check-inline"}))
    class Meta:
        model = Review
        fields = [
            "content",
            "rating"
        ]
        labels = {
            "content": _("Review")
        }