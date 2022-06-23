from rest_framework import viewsets
from filemanager.models import FileManager
from filemanager.serializers import FileManagerSerializer

class FileManagerViewSet(viewsets.ModelViewSet):
       queryset = FileManager.objects.all()
       serializer_class = FileManagerSerializer