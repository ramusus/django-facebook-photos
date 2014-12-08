# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase
from facebook_pages.factories import PageFactory
from facebook_users.models import User

from .factories import AlbumFactory, PhotoFactory
from .models import Album, Photo, Comment

PAGE_ID = 40796308305
ALBUM_ID = 10153647747263306
ALBUM_ID_2 = 892841980756751
PHOTO_ID = 10150131888543306


class FacebookAlbumTest(TestCase):

    def test_fetch_page_albums(self):

        page = PageFactory(graph_id=PAGE_ID)

        self.assertEqual(Album.objects.count(), 0)

        albums = page.fetch_albums(all=True)
        albums_count = Album.objects.count()

        self.assertGreater(len(albums), 0)
        self.assertEqual(albums_count, len(albums))
        self.assertEqual(albums[0].author, page)

        # testing `since` parameter
        Album.objects.all().delete()
        albums = Album.remote.fetch_page(page=page, since=datetime.now() - timedelta(30))
        self.assertLess(albums.count(), albums_count)

        # testing `until` parameter
        Album.objects.all().delete()
        albums = Album.remote.fetch_page(page=page, until=datetime.now() - timedelta(30))
        self.assertLess(albums.count(), albums_count)

    def test_album_fetch_limit(self):
        page = PageFactory(graph_id=PAGE_ID)
        albums = Album.remote.fetch_page(page=page, limit=5)
        self.assertEqual(len(albums), 5)

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

        self.assertGreater(users.count(), 15)
        self.assertEqual(users.count(), User.objects.count())
        self.assertEqual(users.count(), album.shares_users.count())
        self.assertEqual(users.count(), album.shares_count)

    def test_album_fetch_comments(self):
        #album = AlbumFactory(graph_id=ALBUM_ID_2)
        album = Album.remote.fetch(ALBUM_ID_2)

        self.assertEqual(album.wall_comments.count(), 0)
        self.assertEqual(Comment.objects.count(), 0)

        comments = album.fetch_comments(all=True)

        self.assertGreater(comments.count(), 15)
        self.assertEqual(comments.count(), Comment.objects.count())
        self.assertEqual(comments.count(), album.wall_comments.count())
        self.assertEqual(comments.count(), album.comments_count)

        self.assertIsInstance(comments[0].author, User)
        self.assertEqual(comments[0].owner, album)
        self.assertEqual(comments[0].owner_id, album.graph_id)


class FacebookPhotoTest(TestCase):

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
        photos = album.fetch_photos(since=datetime.now() - timedelta(30))
        self.assertLess(photos.count(), photos_count)

        # testing `until` parameter
        Photo.objects.all().delete()
        photos = album.fetch_photos(until=datetime.now() - timedelta(30))
        self.assertLess(photos.count(), photos_count)

    def test_photo_fetch_limit(self):
        album = AlbumFactory(graph_id=ALBUM_ID)
        photos1 = Photo.remote.fetch_album(album=album, limit=5)
        self.assertEqual(len(photos1), 5)

        # offset test
        photos2 = Photo.remote.fetch_album(album=album, limit=5, offset=4)

        self.assertEqual(photos1[4].pk, photos2[0].pk)

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

        self.assertGreater(users.count(), 240)
        self.assertEqual(users.count(), User.objects.count())
        self.assertEqual(users.count(), photo.shares_users.count())
        self.assertEqual(users.count(), photo.shares_count)

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
