# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from random import randint

from django.db.models import Min
from django.utils import timezone
from facebook_pages.factories import PageFactory
from facebook_users.models import User
from facebook_api.tests import FacebookApiTestCase

from .factories import AlbumFactory, PhotoFactory
from .models import Album, Photo, Comment


PAGE_ID = 40796308305
ALBUM_ID = 10153647747263306
ALBUM_ID_2 = 892841980756751
PHOTO_ID = 10150131888543306


class FacebookAlbumTest(FacebookApiTestCase):

    def test_fetch_page_albums(self):

        page = PageFactory(graph_id=PAGE_ID)

        self.assertEqual(Album.objects.count(), 0)

        albums = page.fetch_albums(all=True)
        albums_count = Album.objects.count()

        self.assertGreater(albums.count(), 1500)
        self.assertEqual(albums.count(), albums_count)
        self.assertEqual(albums[0].author, page)

        since = albums.order_by('created_time')[100].created_time
        until = albums.order_by('-created_time')[100].created_time
        self.assertLess(since, until)

        # testing `since` parameter
        albums_since = page.fetch_albums(all=True, since=since)
        self.assertLess(albums_since.count(), albums.count())

        # testing `until` parameter
        albums_until = page.fetch_albums(all=True, since=since, until=until)
        self.assertLess(albums_until.count(), albums_since.count())

    def test_album_fetch_limit(self):
        page = PageFactory(graph_id=PAGE_ID)
        albums = Album.remote.fetch_page(page=page, limit=5)
        self.assertEqual(albums.count(), 5)

    def test_album_fetch_likes(self):
        album = AlbumFactory(graph_id=ALBUM_ID)

        users = album.fetch_likes(all=True)

        self.assertGreater(users.count(), 5)
        self.assertEqual(users.count(), User.objects.count())
        self.assertEqual(users.count(), album.likes_users.count())
        self.assertEqual(users.count(), album.likes_count)

    def test_album_fetch_shares(self):
        album = Album.remote.fetch(ALBUM_ID_2)

        self.assertEqual(album.shares_users.count(), 0)
        self.assertEqual(User.objects.count(), 0)

        users = album.fetch_shares(all=True)

        self.assertGreaterEqual(users.count(), 1)
        self.assertEqual(users.count(), User.objects.count())
        self.assertEqual(users.count(), album.shares_users.count())
        self.assertEqual(users.count(), album.shares_count)

    def test_album_fetch_comments(self):
        album = AlbumFactory(graph_id=ALBUM_ID_2)

        self.assertEqual(album.wall_comments.count(), 0)
        self.assertEqual(Comment.objects.count(), 0)

        comments = album.fetch_comments(all=True)

        self.assertGreaterEqual(comments.count(), 15)
        self.assertEqual(comments.count(), Comment.objects.count())
        self.assertEqual(comments.count(), album.wall_comments.count())
        self.assertEqual(comments.count(), album.comments_count)

        self.assertIsInstance(comments[0].author, User)
        self.assertEqual(comments[0].owner, album)
        self.assertEqual(comments[0].owner_id, album.graph_id)


class FacebookPhotoTest(FacebookApiTestCase):

    def test_fetch_album_counts(self):
        album = AlbumFactory(graph_id=ALBUM_ID)

        for i in range(0, 100):
            PhotoFactory(album=album, likes_count=randint(0, 100),
                         comments_count=randint(0, 100),
                         shares_count=randint(0, 100))

        self.assertEqual(album.likes_count, None)
        self.assertEqual(album.comments_count, None)
        self.assertEqual(album.shares_count, None)

        album.update()

        self.assertGreater(album.likes_count, 0)
        self.assertGreater(album.comments_count, 0)
        self.assertGreater(album.shares_count, 0)

    def test_fetch_album_photos(self):
        album = Album.remote.fetch(ALBUM_ID)

        self.assertEqual(Photo.objects.count(), 0)

        photos = album.fetch_photos(all=True)
        photos_count = Photo.objects.count()

        self.assertGreater(photos.count(), 100)
        self.assertEqual(photos.count(), album.photos_count)
        self.assertEqual(photos.count(), Photo.objects.count())
        self.assertAlmostEqual(photos[0].album_id, int(album.graph_id))

        # testing `since` parameter
        Photo.objects.all().delete()
        since = datetime.now() - timedelta(30)
        photos = album.fetch_photos(since=since)
        self.assertLess(photos.count(), photos_count)

        # testing `until` parameter
        Photo.objects.all().delete()
        until = datetime.now() - timedelta(30)
        photos = album.fetch_photos(until=until, since=since)
        self.assertLess(photos.count(), photos_count)

    def test_fetch_album_photos_reduce_the_amount_error(self):
        since = datetime(2015, 1, 3).replace(tzinfo=timezone.utc)

        album = AlbumFactory(graph_id=338121134579)
        photos = album.fetch_photos(since=since)
        self.assertLessEqual(photos.count(), 30)

        photos = album.fetch_photos(since=since, all=True)
        self.assertGreater(photos.count(), 220)
        self.assertGreater(photos.aggregate(Min('created_time'))['created_time__min'], since)

        # photos = album.fetch_photos(since=since, limit=200)
        # self.assertEqual(photos.count(), 200)  # TODO: 33!=200 Implement fetching requested amount of posts

    def test_photo_fetch_limit(self):
        album = AlbumFactory(graph_id=ALBUM_ID)
        photos1 = Photo.remote.fetch_album(album=album, limit=5)
        self.assertEqual(photos1.count(), 5)

        # TODO: offset test doesn't work
        # photos2 = Photo.remote.fetch_album(album=album, limit=5, offset=4)
        # self.assertEqual(photos1[4].pk, photos2[0].pk)

    def test_photo_fetch_likes(self):
        photo = Photo.remote.fetch(PHOTO_ID)

        self.assertEqual(photo.likes_users.count(), 0)
        self.assertEqual(User.objects.count(), 0)

        users = photo.fetch_likes(all=True)

        self.assertGreater(photo.likes_count, 1500)
        self.assertEqual(users.count(), User.objects.count())
        self.assertEqual(users.count(), photo.likes_users.count())
        self.assertEqual(users.count(), photo.likes_count)

    def test_photo_fetch_shares(self):
        photo = Photo.remote.fetch(PHOTO_ID)

        self.assertEqual(photo.shares_users.count(), 0)
        self.assertEqual(User.objects.count(), 0)

        users = photo.fetch_shares(all=True)

        # self.assertGreaterEqual(users.count(), 233)  # TODO: returns 0
        # self.assertEqual(users.count(), User.objects.count())
        # self.assertEqual(users.count(), photo.shares_users.count())
        # self.assertEqual(users.count(), photo.shares_count)

    def test_photo_fetch_comments(self):
        photo = Photo.remote.fetch(PHOTO_ID)

        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(photo.wall_comments.count(), 0)

        comments = photo.fetch_comments(all=True)

        self.assertGreater(comments.count(), 100)
        self.assertEqual(comments.count(), Comment.objects.count())
        self.assertEqual(comments.count(), photo.wall_comments.count())
        self.assertEqual(comments.count(), photo.comments_count)

        self.assertIsInstance(comments[0].author, User)
        self.assertEqual(comments[0].owner, photo)
        self.assertEqual(comments[0].owner_id, photo.graph_id)


class FacebookPhotosTest(FacebookAlbumTest, FacebookPhotoTest):
    pass
