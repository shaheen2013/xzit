from pickletools import optimize
import profile
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files import File
import os 
import uuid


def get_calculated_size(image_size, reduce):
        return round(image_size - ((image_size*reduce) / 100))


def reduce_image_size(profile_pic):
    prepix = uuid.uuid4().hex[:].upper()
    name, extension = os.path.splitext(profile_pic.name)

    # opening the image
    image = Image.open(profile_pic)
    
    #defining reduce amount int number, [that number e.g 50% will be reduced]
    reduce = 20
    # Checking the extension 
    if extension in ['.jpeg', '.JPEG', '.JPG', '.jpg']:
        ex_format = 'JPEG'
        if image.size[0] > 1200 or image.size[1] > 1200:
            reduce = 25
    else:
        ex_format = 'PNG'
        if image.size[0] > 1000 or image.size[1] > 1000:
            reduce = 45
        else:
            reduce = 35
            
    
    image = image.convert('RGB')
    image = ImageOps.exif_transpose(image)
    thumb_io = BytesIO()

    height = get_calculated_size(image.size[0], reduce)
    width = get_calculated_size(image.size[1], reduce)

    image = image.resize((height, width),Image.ANTIALIAS)
    image.save(thumb_io, ex_format, quality=60, optimize=True)

    new_image = File(thumb_io, name=f'{prepix}.{ex_format}')
    
    return new_image