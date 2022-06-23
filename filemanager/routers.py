from rest_framework.routers import DefaultRouter
from filemanager.viewsets import FileManagerViewSet

router = DefaultRouter()
router.register(r'files', FileManagerViewSet, basename='filemanager')