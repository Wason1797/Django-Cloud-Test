from PersonService import views
from django.urls import path

urlpatterns = [
    path('person/',
         views.PersonView.as_view()),
]
