# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils import timezone
from django.utils.translation import ugettext as _
#from vkontakte_api.utils import api_call
#from vkontakte_api import fields
#from vkontakte_api.models import VkontakteTimelineManager, VkontakteModel, VkontakteCRUDModel
#rom vkontakte_api.decorators import fetch_all
#from vkontakte_users.models import User
#from vkontakte_groups.models import Group
#from parser import VkontaktePhotosParser
import logging
import re

from facebook_api import fields
from facebook_api.models import FacebookGraphModel, FacebookGraphManager #
from facebook_api.utils import graph
from facebook_users.models import User
from facebook_pages.models import Page as Group
from facebook_posts.models import get_or_create_from_small_resource


log = logging.getLogger('facebook_photos')

ALBUM_TYPE_CHOCIES = (
    (0, u'Все пользователи'),
    (1, u'Только друзья'),
    (2, u'Друзья и друзья друзей'),
    (3, u'Только я')
)


# TODO: in develop
class FBModelManager(models.Manager):
    def get_by_natural_key(self, graph_id):
        return self.get(graph_id=graph_id)



class AlbumRemoteManager(FacebookGraphManager):

    @transaction.commit_on_success
    def fetch(self, graph_id=None, user=None, page=None, ids=None, need_covers=False, before=None, after=None, **kwargs):
        if not (graph_id or user or page):
            raise ValueError("You must specify user or page, which albums you want to fetch")

#        kwargs = {
#            #need_covers
#            #1 - будет возвращено дополнительное поле thumb_src. По умолчанию поле thumb_src не возвращается.
#            'need_covers': int(need_covers)
#        }
#        #uid
#        #ID пользователя, которому принадлежат альбомы. По умолчанию – ID текущего пользователя.
#        if user:
#            kwargs.update({'uid': user.remote_id})
#        #gid
#        #ID группы, которой принадлежат альбомы.
#        if group:
#            kwargs.update({'gid': group.remote_id})
#        #aids
#        #перечисленные через запятую ID альбомов.
#        if ids:
#            kwargs.update({'aids': ','.join(map(str, ids))})
#
#        # special parameters
#        kwargs['after'] = after
#        kwargs['before'] = before
        if graph_id:
            return super(AlbumRemoteManager, self).fetch(graph_id)
        elif page:
            ids = []
            #q = "%s/albums/" % page
            response = graph("%s/albums/" % page, **kwargs)
            #log.debug('response objects count - %s' % len(response.data))

            for resource in response.data:
                instance = self.get_or_create_from_resource(resource)
                ids += [instance.pk]

            return Album.objects.filter(pk__in=ids), response



class PhotoRemoteManager(FacebookGraphManager):

    @transaction.commit_on_success
    def fetch(self, graph_id=None, album=None, ids=None, limit=1000, extended=False, offset=0, photo_sizes=False, before=None, rev=0, after=None, **kwargs):
        if ids and not isinstance(ids, (tuple, list)):
            raise ValueError("Attribute 'ids' should be tuple or list")
        if before and not after:
            raise ValueError("Attribute `before` should be specified with attribute `after`")
        if before and before < after:
            raise ValueError("Attribute `before` should be later, than attribute `after`")

        kwargs = {
            #'album': album,
            'extended': int(extended),
            'offset': int(offset),
        }
#        if album.owner:
#            kwargs.update({'uid': album.owner.remote_id})
#        elif album.group:
#            kwargs.update({'gid': album.group.remote_id})
#        if ids:
#            kwargs.update({'photo_ids': ','.join(map(str, ids))})
#        if limit:
#            kwargs.update({'limit': limit})
#
#        kwargs['rev'] = int(rev)

        # special parameters
        kwargs['after'] = after
        kwargs['before'] = before

        # TODO: добавить поля
        #feed
        #Unixtime, который может быть получен методом newsfeed.get в поле date, для получения всех фотографий загруженных пользователем в определённый день либо на которых пользователь был отмечен. Также нужно указать параметр uid пользователя, с которым произошло событие.
        #feed_type
        #Тип новости получаемый в поле type метода newsfeed.get, для получения только загруженных пользователем фотографий, либо только фотографий, на которых он был отмечен. Может принимать значения photo, photo_tag.

        if graph_id:
            return super(PhotoRemoteManager, self).fetch(graph_id)
        elif album:
            if isinstance(album, int):
                album = Album.objects.get(pk=album)
            album_id = album.graph_id


            ids = []
            response = graph("%s/photos" % album_id, limit=limit)
            #log.debug('response objects count - %s' % len(response.data))

            for resource in response.data:
                instance = self.get_or_create_from_resource(resource)
                instance.album = album
                instance.save()
                ids += [instance.pk]

            return Photo.objects.filter(pk__in=ids), response



        return super(PhotoRemoteManager, self).fetch(**kwargs)




#class PhotosAbstractModel(FacebookGraphModel):
#    class Meta:
#        abstract = True
#
#    methods_namespace = 'photos'
#
#    remote_id = models.CharField(u'ID', max_length='20', help_text=u'Уникальный идентификатор', unique=True)
#
#    @property
#    def remote_id_short(self):
#        return self.remote_id.split('_')[1]
#
#    @property
#    def slug(self):
#        return self.slug_prefix + str(self.remote_id)
#
#    def get_remote_id(self, id):
#        '''
#        Returns unique remote_id, contains from 2 parts: remote_id of owner or group and remote_id of photo object
#        TODO: перейти на ContentType и избавиться от метода
#        '''
#        if self.owner:
#            remote_id = self.owner.remote_id
#        elif self.group:
#            remote_id = -1 * self.group.remote_id
#
#        return '%s_%s' % (remote_id, id)
#
#    def parse(self, response):
#        # TODO: перейти на ContentType и избавиться от метода
#        owner_id = int(response.pop('owner_id'))
#        if owner_id > 0:
#            self.owner = User.objects.get_or_create(remote_id=owner_id)[0]
#        else:
#            self.group = Group.objects.get_or_create(remote_id=abs(owner_id))[0]
#
#        super(PhotosAbstractModel, self).parse(response)
#
#        self.remote_id = self.get_remote_id(self.remote_id)


class FacebookGraphIDModel(FacebookGraphModel):

    graph_id = models.BigIntegerField(u'ID', primary_key=True, unique=True, max_length=100, help_text=_('Unique graph ID'))

    def get_url(self, slug=None):
        if slug is None:
            slug = self.graph_id
        return 'http://facebook.com/%s' % slug

    def _substitute(self, old_instance):
        return None

    @property
    def id(self):
        return self.graph_id # return self.pk

    class Meta:
        abstract = True



class AuthorMixin(models.Model):
    author_json = fields.JSONField(null=True, help_text='Information about the user who posted the message') # object containing the name and Facebook id of the user who posted the message

    author_content_type = models.ForeignKey(ContentType, null=True) # , related_name='facebook_albums'
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



class Album(AuthorMixin, FacebookGraphIDModel):
    #remote_pk_field = 'aid'
    #slug_prefix = 'album'


    can_upload = models.BooleanField()
    count = models.PositiveIntegerField(u'Кол-во фотографий', default=0)
    cover_photo = models.CharField(max_length='200')
    link = models.URLField(max_length=255)
    location = models.CharField(max_length='200')
    place = models.CharField(max_length='200') # page
    privacy = models.CharField(max_length='200')
    type = models.CharField(max_length='200')

    # TODO: migrate to ContentType framework, remove vkontakte_users and vkontakte_groups dependencies
    #owner = models.ForeignKey(User, verbose_name=u'Владелец альбома', null=True, related_name='photo_albums')
    #group = models.ForeignKey(Group, verbose_name=u'Группа альбома', null=True, related_name='photo_albums')

    name = models.CharField(max_length='200')
    description = models.TextField()

    created_time = models.DateTimeField(null=True, db_index=True)
    updated_time = models.DateTimeField(null=True, db_index=True)


    objects = models.Manager()
    remote = AlbumRemoteManager()
#    remote = AlbumRemoteManager(remote_pk=('remote_id',), methods={
#        'get': 'getAlbums',
##        'edit': 'editAlbum',
#    })

#    @property
#    def from(self):
#        return self.owner

    class Meta:
        verbose_name = u'Альбом фотографий Facebook'
        verbose_name_plural = u'Альбомы фотографий Facebook'

    def __unicode__(self):
        return self.name


#    @transaction.commit_on_success
    def fetch_photos(self, *args, **kwargs):
        return Photo.remote.fetch(album=self, *args, **kwargs)




class Photo(AuthorMixin, FacebookGraphIDModel):
    album = models.ForeignKey(Album, verbose_name=u'Альбом', related_name='photos', null=True)

    # TODO: switch to ContentType, remove owner and group foreignkeys
    #owner = models.ForeignKey(User, verbose_name=u'Владелец фотографии', null=True, related_name='photos')
    #group = models.ForeignKey(Group, verbose_name=u'Группа фотографии', null=True, related_name='photos')

    #user = models.ForeignKey(User, verbose_name=u'Автор фотографии', null=True, related_name='photos_author')
    link = models.URLField(max_length=255)
    picture = models.URLField(max_length=255) #Link to the 100px wide representation of this photo
    source = models.URLField(max_length=255)

    name = models.CharField(max_length=200, blank=True)
    place = models.CharField(max_length=200, blank=True) # Page

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
#    remote = PhotoRemoteManager(remote_pk=('remote_id',), methods={
#        'get': 'get',
#    })


    class Meta:
        verbose_name = u'Фотография Facebook'
        verbose_name_plural = u'Фотографии Facebook'


    def parse(self, response):
        if 'album' in response:
            print response["album"]
            self.album = response["album"]

        super(Photo, self).parse(response)


#
#        # counters
#        for field_name in ['likes','comments','tags']:
#            if field_name in response and 'count' in response[field_name]:
#                setattr(self, '%s_count' % field_name, response[field_name]['count'])
#
#        self.actions_count = self.likes_count + self.comments_count
#
#        if 'user_id' in response:
#            self.user = User.objects.get_or_create(remote_id=response['user_id'])[0]
#
#        try:
#            self.album = Album.objects.get(remote_id=self.get_remote_id(response['aid']))
#        except Album.DoesNotExist:
#            raise Exception('Impossible to save photo for unexisted album %s' % (self.get_remote_id(response['aid']),))
#
#    def fetch_comments_parser(self):
#        '''
#        Fetch total ammount of comments
#        TODO: implement fetching comments
#        '''
#        post_data = {
#            'act':'photo_comments',
#            'al': 1,
#            'offset': 0,
#            'photo': self.remote_id,
#        }
#        #parser = VkontaktePhotosParser().request('/al_photos.php', data=post_data)
#
#        self.comments_count = len(parser.content_bs.findAll('div', {'class': 'clear_fix pv_comment '}))
#        self.save()
#
#    def fetch_likes_parser(self):
#        '''
#        Fetch total ammount of likes
#        TODO: implement fetching users who likes
#        '''
#        post_data = {
#            'act':'a_get_stats',
#            'al': 1,
#            'list': 'album%s' % self.album.remote_id,
#            'object': 'photo%s' % self.remote_id,
#        }
#        #parser = VkontaktePhotosParser().request('/like.php', data=post_data)
#
#        values = re.findall(r'value="(\d+)"', parser.html)
#        if len(values):
#            self.likes_count = int(values[0])
#            self.save()
#
#    @transaction.commit_on_success
#    def fetch_likes(self, *args, **kwargs):
#
##        kwargs['offset'] = int(kwargs.pop('offset', 0))
#        kwargs['likes_type'] = 'photo'
#        kwargs['item_id'] = self.remote_id.split('_')[1]
#        kwargs['owner_id'] = self.group.remote_id
#        if isinstance(self.group, Group):
#            kwargs['owner_id'] *= -1
#
#        log.debug('Fetching likes of %s %s of owner "%s"' % (self._meta.module_name, self.remote_id, self.group))
#
#        users = User.remote.fetch_instance_likes(self, *args, **kwargs)
#
#        # update self.likes
#        self.likes_count = self.like_users.count()
#        self.save()
#
#        return users
#
#    @transaction.commit_on_success
#    def fetch_comments(self, *args, **kwargs):
#        return Comment.remote.fetch_photo(photo=self, *args, **kwargs)



#import signals
