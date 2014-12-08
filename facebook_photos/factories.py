from django.utils import timezone
import factory
import models


class AlbumFactory(factory.DjangoModelFactory):

    graph_id = factory.Sequence(lambda n: n)
    created_time = factory.LazyAttribute(lambda o: timezone.now())
    updated_time = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Album


class PhotoFactory(factory.DjangoModelFactory):

    graph_id = factory.Sequence(lambda n: n)
    album = factory.SubFactory(AlbumFactory)
    created_time = factory.LazyAttribute(lambda o: timezone.now())
    updated_time = factory.LazyAttribute(lambda o: timezone.now())
    width = 10
    height = 10

    class Meta:
        model = models.Photo
