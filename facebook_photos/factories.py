from django.utils import timezone
import factory
from models import Album, Photo


class AlbumFactory(factory.DjangoModelFactory):
    created_time = timezone.now()
    updated_time = timezone.now()

    class Meta:
        model = Album


class PhotoFactory(factory.DjangoModelFactory):
    album = factory.SubFactory(AlbumFactory)

    created_time = timezone.now()
    updated_time = timezone.now()
    width = 10
    height = 10

    class Meta:
        model = Photo
