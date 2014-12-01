# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase
from facebook_pages.factories import PageFactory
import simplejson as json

from .factories import AlbumFactory, PhotoFactory
from .models import Album, Photo, Comment

PAGE_ID = 40796308305
ALBUM_ID = 10153647747263306
ALBUM_ID_2 = 892841980756751
PHOTO_ID = 10150131888543306


class FacebookAlbumsTest(TestCase):

    def setUp(self):
        self.objects_to_delete = []

    def tearDown(self):
        for object in self.objects_to_delete:
            object.delete(commit_remote=True)

    def test_fetch_albums_by_page(self):

        page = PageFactory(graph_id=PAGE_ID)

        self.assertEqual(Album.objects.count(), 0)

        albums = Album.remote.fetch_by_page(page=page)
        albums_count = Album.objects.count()

        self.assertGreater(len(albums), 0)
        self.assertEqual(albums_count, len(albums))
        self.assertEqual(albums[0].author, page)

        # testing `since` parameter
        Album.objects.all().delete()
        albums = Album.remote.fetch_by_page(page=page, since=datetime.now() - timedelta(30))
        albums_count1 = Album.objects.count()
        self.assertLess(albums_count1, albums_count)
        self.assertEqual(albums_count1, len(albums))

        # testing `until` parameter
        Album.objects.all().delete()
        albums = Album.remote.fetch_by_page(page=page, until=datetime.now() - timedelta(30))
        albums_count1 = Album.objects.count()
        self.assertLess(albums_count1, albums_count)
        self.assertEqual(albums_count1, len(albums))

    def test_likes_and_comments_count(self):
        a = Album.remote.fetch(ALBUM_ID)
        self.assertGreater(a.likes_count, 0)
        self.assertGreater(a.comments_count, 0)

    def test_fetch_limit(self):
        page = PageFactory(graph_id=PAGE_ID)
        albums = Album.remote.fetch_by_page(page=page, limit=5)
        self.assertEqual(len(albums), 5)

    def test_fetch_comments(self):
        #album = AlbumFactory(graph_id=ALBUM_ID_2)
        album = Album.remote.fetch(ALBUM_ID_2)

        self.assertEqual(Comment.objects.count(), 0)

        comments = album.fetch_comments(all=True)
        self.assertGreater(album.comments_count, 15)
        self.assertEqual(album.comments_count, Comment.objects.count())
        self.assertEqual(album.comments_count, len(comments))
        self.assertEqual(album.comments_count, album.album_comments.count())

        self.assertAlmostEqual(comments[0].album_id, int(album.graph_id))


class FacebookPhotosTest(TestCase):

    def test_fetch_album_photos(self):
        album = Album.remote.fetch(ALBUM_ID_2)

        self.assertEqual(Photo.objects.count(), 0)

        photos = album.fetch_photos()

        self.assertGreater(len(photos), 0)
        if album.photos_count <= 100:
            self.assertEqual(len(photos), album.photos_count)
        self.assertEqual(Photo.objects.count(), len(photos))
        self.assertAlmostEqual(photos[0].album_id, int(album.graph_id))

    def test_likes_and_comments_count(self):
        p = Photo.remote.fetch(PHOTO_ID)
        self.assertGreater(p.likes_count, 1000)
        self.assertGreater(p.comments_count, 300)

    def test_fetch_limit(self):
        album = AlbumFactory(graph_id=ALBUM_ID)
        photos1 = Photo.remote.fetch_by_album(album=album, limit=5)
        self.assertEqual(len(photos1), 5)

        # offset test
        photos2 = Photo.remote.fetch_by_album(album=album, limit=5, offset=4)

        self.assertEqual(photos1[4].pk, photos2[0].pk)

    def test_fetch_comments(self):
        photo = Photo.remote.fetch(PHOTO_ID)

        self.assertEqual(Comment.objects.count(), 0)

        comments = photo.fetch_comments(all=True)
        self.assertGreater(photo.comments_count, 100)
        self.assertEqual(photo.comments_count, Comment.objects.count())
        self.assertEqual(photo.comments_count, len(comments))
        self.assertEqual(photo.comments_count, photo.photo_comments.count())

        self.assertAlmostEqual(comments[0].photo_id, int(photo.graph_id))
