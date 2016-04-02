# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models import Sum
from facebook_api.decorators import fetch_all, atomic, memoize
from facebook_api.fields import JSONField
from facebook_api.mixins import (OwnerableModelMixin, AuthorableModelMixin, LikableModelMixin, ShareableModelMixin,
                                 ActionableModelMixin)
from facebook_api.models import FacebookGraphIntPKModel, FacebookGraphTimelineManager
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


class AlbumRemoteManager(FacebookGraphTimelineManager):

    @atomic
    @fetch_all(paging_next_arg_name='after')
    def fetch_page(self, page, limit=1000, **kwargs):
        kwargs.update({
            'limit': int(limit),
        })
        albums = self.fetch("%s/albums" % page.graph_id, **kwargs)
        return albums, self.response


class PhotoRemoteManager(FacebookGraphTimelineManager):

    def update_photos_count_and_get_photos(self, instances, album, *args, **kwargs):
        album.photos_count = album.photos.count()
        album.save()
        return instances

    @atomic
    @fetch_all(return_all=update_photos_count_and_get_photos, paging_next_arg_name='after')
    def fetch_album(self, album, limit=100, offset=0, **kwargs):
        kwargs.update({
            'limit': int(limit),
            'offset': int(offset),
            'extra_fields': {"album_id": album.pk}
        })
        photos = self.fetch("%s/photos" % album.pk, **kwargs)
        return photos, self.response


class Album(OwnerableModelMixin, AuthorableModelMixin, LikableModelMixin, CommentableModelMixin, ShareableModelMixin,
            ActionableModelMixin, FacebookGraphIntPKModel):

    can_upload = models.NullBooleanField()
    photos_count = models.PositiveIntegerField(null=True)
    cover_photo_id = models.BigIntegerField(null=True)  # Photo
    link = models.URLField(max_length=255)
    location = models.CharField(max_length=200)
    place = JSONField(null=True, blank=True)  # page
    privacy = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    name = models.CharField(max_length=200)
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

    def update(self):
        self.update_likes_count()
        self.update_comments_count()
        self.update_shares_count()

    def update_likes_count(self):
        self.likes_count = self.photos.aggregate(Sum('likes_count'))['likes_count__sum']

    def update_comments_count(self):
        self.comments_count = self.photos.aggregate(Sum('comments_count'))['comments_count__sum']

    def update_shares_count(self):
        self.shares_count = self.photos.aggregate(Sum('shares_count'))['shares_count__sum']


class Photo(AuthorableModelMixin, LikableModelMixin, CommentableModelMixin, ShareableModelMixin,
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
