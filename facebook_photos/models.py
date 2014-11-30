# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import re
import time

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext as _
from facebook_api import fields
from facebook_api.decorators import fetch_all, atomic
from facebook_api.models import FacebookGraphIntPKModel, FacebookGraphStrPKModel, FacebookGraphManager
from facebook_api.utils import graph
from facebook_pages.models import Page
from facebook_posts.models import get_or_create_from_small_resource
from facebook_users.models import User
from m2m_history.fields import ManyToManyHistoryField


log = logging.getLogger('facebook_photos')


class AlbumRemoteManager(FacebookGraphManager):

    @atomic
    def fetch_by_page(self, page, limit=1000, until=None, since=None, **kwargs):

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
        response = graph("%s/albums/" % page.graph_id, **kwargs)
        #log.debug('response objects count - %s' % len(response.data))

        for resource in response.data:
            instance = self.get_or_create_from_resource(resource)
            ids += [instance.pk]

        return Album.objects.filter(pk__in=ids)


class PhotoRemoteManager(FacebookGraphManager):

    @atomic
    def fetch_by_album(self, album, limit=100, offset=0, until=None, since=None, **kwargs):

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
        response = graph("%s/photos" % album.pk, **kwargs)
        #log.debug('response objects count - %s' % len(response.data))

        extra_fields = {"album_id": album.pk}
        for resource in response.data:
            instance = self.get_or_create_from_resource(resource, extra_fields)
            ids += [instance.pk]

        return Photo.objects.filter(pk__in=ids)


class Comment(FacebookGraphStrPKModel):

    album = models.ForeignKey('Album', related_name='album_comments', null=True)
    photo = models.ForeignKey('Photo', related_name='photo_comments', null=True)

    author_json = fields.JSONField(null=True, help_text='Information about the user who posted the comment')  # object containing the name and Facebook id of the user who posted the message

    author_content_type = models.ForeignKey(ContentType, null=True)
    author_id = models.PositiveIntegerField(null=True, db_index=True)
    author = generic.GenericForeignKey('author_content_type', 'author_id')

    message = models.TextField(help_text='The message')
    created_time = models.DateTimeField(help_text='The time the comment was initially published', db_index=True)

    can_remove = models.BooleanField(default=False)
    user_likes = models.BooleanField(default=False)

    #like_users = ManyToManyHistoryField(User, related_name='like_comments')

    objects = models.Manager()
    remote = FacebookGraphManager()

    def _substitute(self, old_instance):
        return None

    def save(self, *args, **kwargs):
        # set exactly right Page or User contentTypes, not a child
        for field_name in ['author']:
            for allowed_model in [Page, User]:
                if isinstance(getattr(self, field_name), allowed_model):
                    setattr(self, '%s_content_type' % field_name, ContentType.objects.get_for_model(allowed_model))
                    break

        # check is generic fields has correct content_type
        if self.author_content_type:
            allowed_ct_ids = [ct.pk for ct in ContentType.objects.get_for_models(Page, User).values()]
            if self.author_content_type.pk not in allowed_ct_ids:
                raise ValueError("'author' field should be Page or User instance")

        return super(Comment, self).save(*args, **kwargs)

    def parse(self, response):
        if 'from' in response:
            response['author_json'] = response.pop('from')
        if 'like_count' in response:
            response['likes_count'] = response.pop('like_count')

# transform graph_id from {POST_ID}_{COMMENT_ID} -> {PAGE_ID}_{POST_ID}_{COMMENT_ID}
#        if response['id'].count('_') == 1:
#            response['id'] = re.sub(r'^\d+', self.post.graph_id, response['id'])

        super(Comment, self).parse(response)

        if self.author is None and self.author_json:
            self.author = get_or_create_from_small_resource(self.author_json)

    class Meta:
        verbose_name = 'Facebook comment'
        verbose_name_plural = 'Facebook comments'


class AuthorMixin(models.Model):

    author_json = fields.JSONField(null=True, help_text='Information about the user who posted the message')  # object containing the name and Facebook id of the user who posted the message

    author_content_type = models.ForeignKey(ContentType, null=True)  # , related_name='facebook_albums'
    author_id = models.PositiveIntegerField(null=True, db_index=True)
    author = generic.GenericForeignKey('author_content_type', 'author_id')

    def parse(self, response):
        if 'from' in response:
            response['author_json'] = response.pop('from')

        super(AuthorMixin, self).parse(response)

        if self.author is None and self.author_json:
            self.author = get_or_create_from_small_resource(self.author_json)

    class Meta:
        abstract = True


class LikesCountMixin(models.Model):

    likes_count = models.IntegerField(null=True, help_text='The number of comments of this item')

    class Meta:
        abstract = True

    def parse(self, response):
        if 'likes' in response:
            response['likes_count'] = len(response['likes']["data"])
        super(LikesCountMixin, self).parse(response)


class CommentsCountMixin(models.Model):

    comments_count = models.IntegerField(null=True, help_text='The number of comments of this item')

    class Meta:
        abstract = True

    def parse(self, response):
        if 'comments' in response:
            response['comments_count'] = len(response['comments']["data"])
        super(CommentsCountMixin, self).parse(response)

    def update_count_and_get_comments(self, instances, *args, **kwargs):
        self.comments_count = instances.count()
        self.save()
        return instances.all()

    @atomic
    #@fetch_all(return_all=update_count_and_get_comments, paging_next_arg_name='after')
    def fetch_comments(self, limit=1000, filter='stream', summary=True, **kwargs):
        '''
        Retrieve and save all comments
        '''
        extra_fields = {('%s_id' % self._meta.module_name): self.pk}  # {"album_id": 1}
        ids = []
        response = graph('%s/comments' % self.graph_id, limit=limit, filter=filter, summary=int(summary), **kwargs)
        if response:
            #log.debug('response objects count=%s, limit=%s, after=%s' % (len(response.data), limit, kwargs.get('after')))
            for resource in response.data:
                instance = Comment.remote.get_or_create_from_resource(resource, extra_fields)
                ids += [instance.pk]

        return Comment.objects.filter(pk__in=ids)


class Album(AuthorMixin, LikesCountMixin, CommentsCountMixin, FacebookGraphIntPKModel):

    can_upload = models.BooleanField()
    photos_count = models.PositiveIntegerField(default=0)
    cover_photo = models.BigIntegerField(null=True)
    link = models.URLField(max_length=255)
    location = models.CharField(max_length='200')
    place = models.CharField(max_length='200')  # page
    privacy = models.CharField(max_length='200')
    type = models.CharField(max_length='200')

    name = models.CharField(max_length='200')
    description = models.TextField()

    created_time = models.DateTimeField(null=True, db_index=True)
    updated_time = models.DateTimeField(null=True, db_index=True)

    objects = models.Manager()
    remote = AlbumRemoteManager()

    class Meta:
        verbose_name = 'Facebook Album'
        verbose_name_plural = 'Facebook Albums'

    def __unicode__(self):
        return self.name


#    @transaction.commit_on_success
    def fetch_photos(self, **kwargs):
        return Photo.remote.fetch_by_album(album=self, **kwargs)

    def parse(self, response):
        response['photos_count'] = response.get("count", 0)
        super(Album, self).parse(response)


class Photo(AuthorMixin, LikesCountMixin, CommentsCountMixin, FacebookGraphIntPKModel):

    album = models.ForeignKey(Album, related_name='photos', null=True)

    # TODO: switch to ContentType, remove owner and group foreignkeys
    #owner = models.ForeignKey(User, verbose_name=u'Владелец фотографии', null=True, related_name='photos')
    #group = models.ForeignKey(Group, verbose_name=u'Группа фотографии', null=True, related_name='photos')

    #user = models.ForeignKey(User, verbose_name=u'Автор фотографии', null=True, related_name='photos_author')
    link = models.URLField(max_length=255)
    picture = models.URLField(max_length=255)  # Link to the 100px wide representation of this photo
    source = models.URLField(max_length=255)

    name = models.CharField(max_length=200, blank=True)
    place = models.CharField(max_length=200, blank=True)  # Page

    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)

#    likes_count = models.PositiveIntegerField(u'Лайков', default=0)
#    comments_count = models.PositiveIntegerField(u'Комментариев', default=0)
#    actions_count = models.PositiveIntegerField(u'Комментариев', default=0)
#    tags_count = models.PositiveIntegerField(u'Тегов', default=0)
#
#    like_users = models.ManyToManyField(User, related_name='like_photos')

    created_time = models.DateTimeField(db_index=True)
    updated_time = models.DateTimeField(db_index=True)

    objects = models.Manager()
    remote = PhotoRemoteManager()

    class Meta:
        verbose_name = 'Facebook Photo'
        verbose_name_plural = u'Facebook Photos'
