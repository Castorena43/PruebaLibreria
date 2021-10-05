from django.urls import path
import api.views as views

urlpatterns = [
    path('libros/', views.get_all_books),
    path('libros/crear/', views.create_libro),
    path('generos/', views.get_all_generos),
    path('autores/', views.get_all_autores),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('libros/search/', views.search)
]