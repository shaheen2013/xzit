from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from filemanager.models import FileManager
from filemanager.serializers import FileManagerSerializer
from rest_framework.permissions import IsAuthenticated


class FileManagerViewSet(viewsets.ModelViewSet):
       queryset = FileManager.objects.all()
       serializer_class = FileManagerSerializer
       parser_classes = (MultiPartParser, )
       permission_classes = [IsAuthenticated]
       

       def get_queryset(self):
        return FileManager.objects.filter(created_by=self.request.user)