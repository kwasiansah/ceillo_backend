from django.contrib import admin
from .models import *

# TODO: i need to work on the admin panel password hashing
# Register your models here.

@admin.register(ProductCatalog)
class AdminProductCatalog(admin.ModelAdmin):
    prepopulated_fields = {'url_slug': ('title',)}

@admin.register(ProductCategory)
class AdminProductCategory(admin.ModelAdmin):
    prepopulated_fields = {'url_slug': ('title',)}

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {'url_slug': ('name',)}

@admin.register(ProductQuestion)
class AdminProductQuestion(admin.ModelAdmin):
    pass
@admin.register(ProductReviews)
class AdminProductReview(admin.ModelAdmin):
    pass

@admin.register(ProductAnswer)
class AdminProductAnswer(admin.ModelAdmin):
    pass