from django.utils import timezone
import factory
import models


class AlbumFactory(factory.DjangoModelFactory):

    created_time = factory.LazyAttribute(lambda o: timezone.now())
    updated_time = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Album


class PhotoFactory(factory.DjangoModelFactory):

    album = factory.SubFactory(AlbumFactory)
    created_time = factory.LazyAttribute(lambda o: timezone.now())
    updated_time = factory.LazyAttribute(lambda o: timezone.now())
    width = 10
    height = 10

    class Meta:
        model = models.Photo
