from rest_framework.views import APIView
from .models import Person
from .serializers import PersonSerializer
from rest_framework.response import Response
# Create your views here.


class PersonView(APIView):

    def get(self, request):
        person_id = request.GET.get('id')
        if person_id is None:
            persons = Person.objects.all()
            serializedPersons = PersonSerializer(persons, many=True)
            return Response(serializedPersons.data, status=200)
        else:
            person = Person.objects.get(person_id=int(person_id))
            serializedPerson = PersonSerializer(person)
            return Response(serializedPerson.data, status=200)

    def post(self, request):
        serializedPerson = PersonSerializer(data=request.data)
        if serializedPerson.is_valid():
            serializedPerson.save()
            return Response({
                "msg": "Person saved correctly",
            }, status=200)
        else:
            return Response({
                "msg": "Error while saving person",
                "errors": serializedPerson.errors
            }, status=200)

    def put(self, request):
        personInstance = Person.objects.get(
            person_id=int(request.data['person_id']))
        serializedPerson = PersonSerializer(personInstance, data=request.data)
        if serializedPerson.is_valid():
            serializedPerson.save()
            return Response({"status": "Person Updated Correctly"}, status=200)
        else:
            return Response({
                "error": True,
                "errors": serializedPerson.errors
            })

    def delete(self, request):
        param = request.GET.get('id')
        if param is not None:
            Person.objects.filter(person_id=int(param)).delete()
            return Response({"status":
                             "Person deleted succesfully"}, status=200)
