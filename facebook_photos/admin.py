# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from models import Album, Photo

class PhotoInline(admin.TabularInline):

    def image(self, instance):
        return '<img src="%s" />' % (instance.src_small,)
    image.short_description = 'photo'
    image.allow_tags = True

    model = Photo
    fields = ('created','image','text','owner','group','user','likes_count','comments_count','tags_count')
    readonly_fields = fields
    extra = False
    can_delete = False

class AlbumAdmin(admin.ModelAdmin):

    list_display = ('name','count', 'owner', 'place', 'privacy', 'type', 'created_time','updated_time')
    list_display_links = ('name',)
    search_fields = ('name','description')
    inlines = [PhotoInline]

class PhotoAdmin(admin.ModelAdmin):

    def image_preview(self, obj):
        return u'<a href="%s"><img src="%s" height="30" /></a>' % (obj.src_big, obj.src)
    image_preview.short_description = u'Картинка'
    image_preview.allow_tags = True

    def text_with_link(self, obj):
        return u'%s <a href="%s"><strong>ссылка</strong></a>' % (obj.text, (reverse('admin:vkontakte_photos_photo_change', args=(obj.id,))))
    text_with_link.short_description = u'Текст'
    text_with_link.allow_tags = True

    list_display = ('image_preview','text_with_link','likes_count','comments_count','tags_count','created')
    list_filter = ('album',)

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
