from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


# TODO: i need to work on the admin panel password hashing
# Register your models here.


@admin.register(Collection)
class AdminCollection(admin.ModelAdmin):
    prepopulated_fields = {'url_slug': ('name',)}
    readonly_fields = ["thumbnail_image"]

    def thumbnail_image(self, obj):

        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.thumbnail.url,
            # width=obj.thumbnail.width,
            # height=obj.thumbnail.height,
            width=200,
            height=200,
        ))


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {'url_slug': ('name',)}
    readonly_fields = ["thumbnail_image"]

    def thumbnail_image(self, obj):

        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.thumbnail.url,
            # width=obj.thumbnail.width,
            # height=obj.thumbnail.height,
            width=200,
            height=200,
        ))


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {'url_slug': ('name',)}
    readonly_fields = ["thumbnail_image"]

    def thumbnail_image(self, obj):

        return mark_safe('<img src="{url}" width="{width}" height={height} /><br><video src="{vid}"   autoplay controls  width=400, height=400></video>'.format(
            url=obj.media.all()[0].raw_image.url,
            # width=obj.thumbnail.width,
            # height=obj.thumbnail.height,
            vid=obj.media.all()[0].video.url,
            width=200,
            height=200,
        ))


@admin.register(ProductQuestion)
class AdminProductQuestion(admin.ModelAdmin):
    pass


@admin.register(ProductReviews)
class AdminProductReview(admin.ModelAdmin):
    pass


@admin.register(ProductAnswer)
class AdminProductAnswer(admin.ModelAdmin):
    pass


@admin.register(ProductMedia)
class AdminProductMedia(admin.ModelAdmin):
    pass
