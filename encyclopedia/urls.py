from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name = 'main'),
    path('home', views.main_page, name = 'main'),
    path('search', views.search, name = 'search'),
    path('create', views.create, name = 'create'),
    path('random', views.random_choice, name = 'random'),
    path('wiki/<str:title>', views.entry, name = 'entry'),
    path('home/<str:title>', views.entry, name = 'entry'),
    path('edit/<str:title>', views.edit, name = 'edit'),
    path("<str:title>", views.entry, name = "loadentry")

]