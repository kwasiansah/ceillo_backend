from .utils.helper_func import get_product_image
from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


# TODO: i need to work on the admin panel password hashing
# Register your models here.

# admin.site.site_header = 'ceillo'


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
    print('category')
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
    readonly_fields = ["thumbnail_image", ]
    filter_horizontal = ('category',)

    @admin.display(description='thumnails')
    def thumbnail_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height}/><br><video src="{vid}"   autoplay controls  width=350, height=350></video>'.format(
            url=get_product_image(obj)[0],
            vid=get_product_image(obj)[1],
            width=200,
            height=200,
        ))
        # return mark_safe('<p>{url}</p><br><p>{vid}</p>'.format(
        #     url=get_product_image(obj)[0],
        #     vid=get_product_image(obj)[0],
        # ))


@admin.register(ProductQuestion)
class AdminProductQuestion(admin.ModelAdmin):
    pass


@admin.register(ProductReviews)
class AdminProductReview(admin.ModelAdmin):
    readonly_fields = ('thumbnail_image',)

    def thumbnail_image(self, obj):

        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            # width=obj.thumbnail.width,
            # height=obj.thumbnail.height,
            width=200,
            height=200,
        ))


@admin.register(ProductAnswer)
class AdminProductAnswer(admin.ModelAdmin):
    pass


@admin.register(ProductMedia)
class AdminProductMedia(admin.ModelAdmin):
    readonly_fields = ('thumbnail_image',)

    @admin.display(description='thumnails')
    def thumbnail_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height}/><br><video src="{vid}"   autoplay controls  width=350, height=350></video>'.format(
            url=obj.raw_image.url,
            vid=obj.video.url,
            width=200,
            height=200,
        ))
