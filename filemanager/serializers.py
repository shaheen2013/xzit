from rest_framework.serializers import ModelSerializer, SerializerMethodField
from filemanager.models import FileManager


class FileManagerSerializer(ModelSerializer):
       size = SerializerMethodField()
       name = SerializerMethodField()
       file_type = SerializerMethodField()
       created_at = SerializerMethodField()

       class Meta:
              model = FileManager
              fields = ('file', 'created_at', 'size', 'name', 'file_type')

       def get_size(self, obj):
              file_size = ''
              if obj.file and hasattr(obj.file, 'size'):
                     file_size = obj.file.size
              return file_size
       
       def get_name(self, obj):
              file_name = ''
              if obj.file and hasattr(obj.file, 'name'):
                     file_name = obj.file.name
              return file_name
       
       def get_file_type(self, obj):
              filename = obj.file.name
              return filename.split('.')[-1]
       def get_created_at(self, obj):
              date_added = obj.created_at
              return date_added