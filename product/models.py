import uuid

from django.db import models

from customer.models import Customer, Merchant
from product.utils.helper_func import get_url_slug
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video

MAX_LENGTH = 1000


class Collection(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, null=False)
    url_slug = models.SlugField()
    thumbnail = models.ImageField(
        upload_to="collection/", default="default/default.jpg"
    )
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.url_slug = get_url_slug(self.name)
        print(self.url_slug)
        super().save(*args, **kwargs)


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )
    name = models.CharField(max_length=MAX_LENGTH, default="", blank=False)
    url_slug = models.SlugField(max_length=250)

    thumbnail = models.ImageField(
        upload_to="Category/", default="default/default.jpg"
    )
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    # thinking of making this a many to many field
    collection = models.ManyToManyField(
        Collection, related_name="categories", blank=True
    )
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        class_ = type(self)
        return "%s(pk=%r, name=%r, product_pk=%r)" % (
            class_.__name__,
            self.pk,
            self.name,
            self.parent.name if self.parent else self.parent,
        )

    def save(self, *args, **kwargs):
        self.url_slug = get_url_slug(self.name)
        print(self.url_slug)
        super().save(*args, **kwargs)


class Product(models.Model):

    product_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        blank=False,
        null=False,
        editable=False,
    )
    name = models.CharField(max_length=MAX_LENGTH, unique=False)
    url_slug = models.SlugField(default="")
    brand = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    stock = models.PositiveIntegerField()
    active = models.BooleanField(default=False)
    # checks if the products is tangible or not
    """ 
    This field would be implemented later
    
    digital = models.BooleanField(default=False)

    """
    merchant = models.ForeignKey(
        Merchant, blank=False, null=True, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    updated = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0.0)
    video_url = models.FileField(
        upload_to="products/video/",
        null=True,
        blank=True,
        default="default/defaultvid.mp4",
        storage=VideoMediaCloudinaryStorage,
        validators=[validate_video],
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        class_ = type(self)
        return "%s(pk=%r, name=%r)" % (
            class_.__name__,
            self.pk,
            self.name,
        )

    def save(self, *args, **kwargs):
        if self.name not in self.url_slug:
            self.url_slug = get_url_slug(self.name)
        print(self.url_slug)
        super().save(*args, **kwargs)


class ProductMedia(models.Model):
    """
    would create a more dynamic location when images have been hosted
    """

    # TODO: remember to change to null = False later

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name="images",
    )
    # this field name must change to image
    image_url = models.ImageField(
        upload_to="products/", default="default/default.jpg"
    )
    thumbnail = models.ImageField(
        upload_to="products/thumbnail/", null=True, blank=True
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)
        verbose_name = "Product Media"
        verbose_name_plural = "Product Media"

    def __str__(self):
        return self.image_url.name

    def save(self, *args, **kwargs):
        if "default" in self.image_url.name:
            print("default image used")
        else:
            print("thumbnail was created")
        super().save(*args, **kwargs)


class ProductQuestion(models.Model):
    """
    i would create a unique id to be used for the individual questions to query the data base and use in the url
    """

    # may be a CharField rather
    question = models.TextField()
    active = models.BooleanField(default=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="questions"
    )
    # added this field to it to tell which customer posted the question
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "Product Question"
        verbose_name_plural = "Product Questions"

    def __repr__(self) -> str:
        class_ = type(self)
        return "%s(pk=%r, name=%r, product_pk=%r)" % (
            class_.__name__,
            self.pk,
            self.question[:12],
            self.created,
        )

    def __str__(self):
        return f"{self.product.name} product questions"


class ProductAnswer(models.Model):
    """
    i would create a unique id to be used for the individual Answer to query the data base and use in the url
    """

    answer = models.TextField()

    question = models.ForeignKey(
        ProductQuestion, on_delete=models.CASCADE, related_name="answers"
    )

    # may be we should protect the answer when the customer is deleted
    # another model should be created to handle the voting
    voting = models.PositiveIntegerField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-updated",)
        verbose_name = "Product Answer"
        verbose_name_plural = "Product Answers"

    def __str__(self):
        return self.answer

    def __repr__(self) -> str:
        class_ = type(self)
        return "%s(pk=%r, answer=%r, question=%r)" % (
            class_.__name__,
            self.pk,
            self.answer[:12],
            self.question.id,
        )


class ProductReviews(models.Model):
    """
    i would create a unique id to be used for the individual reviews to query the data base and use in the url
    """

    image = models.ImageField(
        upload_to="reviews/", default="default/default.jpg"
    )
    # TODO: rating should be a new model
    rating = models.FloatField(
        default=0.0,
    )
    review = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    # I used models.PROTECT to prevent the review from being removed when customer is deleated
    # another thought when a customer is deleted it merchant account is deleted and its product is also deleted meaning protecting the productReveiw is not needed
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="reviews"
    )

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return f"{self.product.name} Reviews"

    def __repr__(self) -> str:
        class_ = type(self)
        return "%s(pk=%r, review=%r, product_pk=%r)" % (
            class_.__name__,
            self.pk,
            self.review[:12],
            self.product.id,
        )
