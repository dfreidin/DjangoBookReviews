from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.login, name="login"),
    url(r'^register$', views.register, name="register"),
    url(r'^books$', views.books, name="books"),
    url(r'^books/(?P<id>\d+)$', views.show_book, name="show_book"),
    url(r'^users/(?P<id>\d+)$', views.show_user, name="show_user"),
    url(r'^add_review/(?P<id>\d+)$', views.add_review, name="add_review"),
    url(r'^delete_review/(?P<id>\d+)$', views.delete_review, name="delete_review"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^add$', views.add, name="add"),
    url(r'^add_book$', views.add_book, name="add_book")
]