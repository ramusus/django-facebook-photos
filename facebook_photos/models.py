# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import re
import time

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
from facebook_api.api import api_call
from facebook_api.decorators import fetch_all, atomic, memoize
from facebook_api.fields import JSONField
from facebook_api.mixins import OwnerableModelMixin, AuthorableModelMixin, LikableModelMixin, ShareableModelMixin, \
    ActionableModelMixin
from facebook_api.models import FacebookGraphIntPKModel, FacebookGraphStrPKModel, FacebookGraphManager
from facebook_api.utils import get_improperly_configured_field

if 'facebook_comments' in settings.INSTALLED_APPS:
    from facebook_comments.models import Comment
    from facebook_comments.mixins import CommentableModelMixin
    wall_comments = generic.GenericRelation(
        Comment, content_type_field='owner_content_type', object_id_field='owner_id', verbose_name=u'Comments')
else:
    wall_comments = get_improperly_configured_field('facebook_comments', True)

    class CommentableModelMixin(models.Model):
        comments_count = None
        fetch_comments = get_improperly_configured_field('facebook_comments')


log = logging.getLogger('facebook_photos')


class AlbumRemoteManager(FacebookGraphManager):

    @atomic
    @fetch_all(always_all=False, paging_next_arg_name='after')
    def fetch_page(self, page, limit=1000, until=None, since=None, **kwargs):

        kwargs.update({
            'limit': int(limit),
        })

        for field in ['until', 'since']:
            value = locals()[field]
            if isinstance(value, datetime):
                kwargs[field] = int(time.mktime(value.timetuple()))
            elif value is not None:
                try:
                    kwargs[field] = int(value)
                except TypeError:
                    raise ValueError('Wrong type of argument %s: %s' % (field, type(value)))

        ids = []
        response = api_call("%s/albums/" % page.graph_id, **kwargs)
        #log.debug('response objects count - %s' % len(response.data))

        for resource in response.data:
            instance = self.get_or_create_from_resource(resource)
            ids += [instance.pk]

        return Album.objects.filter(pk__in=ids), response


class PhotoRemoteManager(FacebookGraphManager):

    def update_photos_count_and_get_photos(self, instances, album, *args, **kwargs):
        album.photos_count = album.photos.count()
        album.save()
        return instances

    @atomic
    @fetch_all(return_all=update_photos_count_and_get_photos, always_all=False, paging_next_arg_name='after')
    def fetch_album(self, album, limit=100, offset=0, until=None, since=None, **kwargs):

        kwargs.update({
            'limit': int(limit),
            'offset': int(offset),
        })

        for field in ['until', 'since']:
            value = locals()[field]
            if isinstance(value, datetime):
                kwargs[field] = int(time.mktime(value.timetuple()))
            elif value is not None:
                try:
                    kwargs[field] = int(value)
                except TypeError:
                    raise ValueError('Wrong type of argument %s: %s' % (field, type(value)))

        ids = []
        response = api_call("%s/photos" % album.pk, **kwargs)
        #log.debug('response objects count - %s' % len(response.data))

        extra_fields = {"album_id": album.pk}
        for resource in response.data:
            instance = self.get_or_create_from_resource(resource, extra_fields)
            ids += [instance.pk]

        return Photo.objects.filter(pk__in=ids), response


class Album(OwnerableModelMixin, AuthorableModelMixin,
            LikableModelMixin, CommentableModelMixin, ShareableModelMixin,
            ActionableModelMixin, FacebookGraphIntPKModel):

    can_upload = models.BooleanField()
    photos_count = models.PositiveIntegerField(null=True)
    cover_photo_id = models.BigIntegerField(null=True)  # Photo
    link = models.URLField(max_length=255)
    location = models.CharField(max_length="200")
    place = JSONField(null=True, blank=True)  # page
    privacy = models.CharField(max_length="200")
    type = models.CharField(max_length="200")

    name = models.CharField(max_length="200")
    description = models.TextField()

    created_time = models.DateTimeField(null=True, db_index=True)
    updated_time = models.DateTimeField(null=True, db_index=True)

    objects = models.Manager()
    remote = AlbumRemoteManager()

    class Meta:
        verbose_name = "Facebook Album"
        verbose_name_plural = "Facebook Albums"

    def __unicode__(self):
        return self.name

    @property
    @memoize
    def cover_photo(self):
        return Photo.objects.get(pk=self.cover_photo_id)

    def fetch_photos(self, **kwargs):
        return Photo.remote.fetch_album(album=self, **kwargs)

    def parse(self, response):
        response["photos_count"] = response.get("count", None)
        response["cover_photo_id"] = response.get("cover_photo", None)
        super(Album, self).parse(response)


class Photo(AuthorableModelMixin,
            LikableModelMixin, CommentableModelMixin, ShareableModelMixin,
            ActionableModelMixin, FacebookGraphIntPKModel):

    album = models.ForeignKey(Album, related_name="photos", null=True)

    link = models.URLField(max_length=255)
    picture = models.URLField(max_length=255)  # Link to the 100px wide representation of this photo
    source = models.URLField(max_length=255)

    name = models.TextField()
    place = JSONField(null=True, blank=True)  # page

    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)

    created_time = models.DateTimeField(null=True, db_index=True)
    updated_time = models.DateTimeField(null=True, db_index=True)

    objects = models.Manager()
    remote = PhotoRemoteManager()

    class Meta:
        verbose_name = 'Facebook Photo'
        verbose_name_plural = u'Facebook Photos'


for Model in [Album, Photo]:
    Model.add_to_class('wall_comments', wall_comments)
