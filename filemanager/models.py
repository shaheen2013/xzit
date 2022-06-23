from django.db import models

from xzit.mixins.models import AuthorMixin, TimeStampMixin

class FileManager(TimeStampMixin, AuthorMixin):
       file = models.FileField(null=True, max_length=255)
       
       def __str__(self) -> str:
              return str(self.file.name)
