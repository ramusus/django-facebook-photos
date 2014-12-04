# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse

from facebook_api.admin import FacebookModelAdmin

from .models import Album, Photo


class PhotoInline(admin.TabularInline):

    def image(self, instance):
        return '<img src="%s" />' % (instance.picture,)
    image.short_description = 'photo'
    image.allow_tags = True

    model = Photo
    fields = ('name', 'place', 'created_time')
    readonly_fields = fields
    extra = False
    can_delete = False


class AlbumAdmin(FacebookModelAdmin):

    list_display = ('name', 'graph_id', 'photos_count', 'likes_count', 'comments_count',
                    'author', 'place', 'privacy', 'type', 'created_time', 'updated_time')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    inlines = [PhotoInline]


class PhotoAdmin(FacebookModelAdmin):

    def image_preview(self, obj):
        return u'<a href="%s"><img src="%s" height="30" /></a>' % (obj.link, obj.picture)
    image_preview.short_description = u'Картинка'
    image_preview.allow_tags = True

#    def text_with_link(self, obj):
#        return u'%s <a href="%s"><strong>ссылка</strong></a>' % (obj.text, (reverse('admin:vkontakte_photos_photo_change', args=(obj.id,))))
#    text_with_link.short_description = u'Текст'
#    text_with_link.allow_tags = True

#    def fb_link(self, obj):
#        return u'<a href="%s">fb_link</a>' % obj.link
#    image_preview.short_description = u'fb_link'
#    image_preview.allow_tags = True

#    def edit_link(self, obj):
#        return u'edit'
#    image_preview.short_description = u'Edit link'

    list_display = ('graph_id', 'image_preview', 'likes_count', 'comments_count', 'name', 'place', 'created_time')
    #list_display_links = ('edit_link',)
    list_filter = ('album',)


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
