from PersonMain import views
from django.urls import path

urlpatterns = [
    path('people',
         views.person_list),
]
