from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

# TODO: i need to work on the admin panel password hashing
# Register your models here.

admin.site.site_header = "ceillo"


@admin.register(Collection)
class AdminCollection(admin.ModelAdmin):
    prepopulated_fields = {"url_slug": ("name",)}
    readonly_fields = ["thumbnail_image"]

    def thumbnail_image(self, obj):

        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.thumbnail.url,
                width=200,
                height=200,
            )
        )


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    print("category")
    prepopulated_fields = {"url_slug": ("name",)}
    readonly_fields = ["thumbnail_image"]

    def thumbnail_image(self, obj):

        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.thumbnail.url,
                width=200,
                height=200,
            )
        )


class ProductMediaInline(admin.StackedInline):
    model = ProductMedia
    readonly_fields = ("thumbnail_image",)
    # to prevent duplicate in the admin panel
    extra = 0

    @admin.display(description="thumnails")
    def thumbnail_image(self, obj):
        print(obj)
        print("passed here")
        return mark_safe(
            '<img src="{url}" width="{width}" height={height}/>'.format(
                url=obj.image_url.url,
                width=200,
                height=200,
            )
        )


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {"url_slug": ("name",)}
    readonly_fields = ("thumbnail_image",)
    inlines = [ProductMediaInline]

    @admin.display(description="thumnails")
    def thumbnail_image(self, obj):
        return mark_safe(
            '<video src="{vid}"   autoplay controls  width={width}, height={height}></video>'.format(
                vid=obj.video_url.url,
                width=350,
                height=350,
            )
        )


@admin.register(ProductQuestion)
class AdminProductQuestion(admin.ModelAdmin):
    pass


@admin.register(ProductReviews)
class AdminProductReview(admin.ModelAdmin):
    readonly_fields = ("thumbnail_image",)

    def thumbnail_image(self, obj):

        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image_url.url,
                width=200,
                height=200,
            )
        )


@admin.register(ProductMedia)
class AdminProductMedia(admin.ModelAdmin):
    readonly_fields = ("thumbnail_image",)

    @admin.display(description="thumnails")
    def thumbnail_image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height}/>'.format(
                url=obj.image_url.url,
                width=200,
                height=200,
            )
        )


@admin.register(ProductAnswer)
class AdminProductAnswer(admin.ModelAdmin):
    pass
