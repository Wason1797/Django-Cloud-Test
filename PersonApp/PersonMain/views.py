from django.shortcuts import render
from PersonService.models import Person
# Create your views here.


def person_list(request):
    persons = Person.objects.all()
    context = {
        'persons': persons
    }
    return render(request, 'person/index.html', context)
