from PIL import Image
from io import BytesIO
from django.core.files import File
import os 
import uuid

def reduce_image_size(profile_pic):
    prepix = uuid.uuid4().hex[:].upper()
    name, extension = os.path.splitext(profile_pic.name)
    if extension == '.jpg':
            format = 'jpeg'
    else:
            format = 'png'
    img = Image.open(profile_pic)
    thumb_io = BytesIO()
    img.save(thumb_io, format=format, quality=50)
    new_image = File(thumb_io, name=prepix+extension)
    return new_image