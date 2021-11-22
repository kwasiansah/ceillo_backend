from django.db import models
import uuid
from customer.models import Customer, Merchant
# Create your models here.


class ProductCatalog(models.Model):

    title = models.CharField(max_length=250, null=False)
    url_slug = models.SlugField()
    thumbnail = models.ImageField(upload_to='catalog/', blank=True, null=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Product Catalog'
        verbose_name_plural = 'Products Catalogs'

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    title = models.CharField(max_length=250, default="", blank=False)
    url_slug = models.SlugField(max_length=250, unique=True)
    thumbnail = models.ImageField(upload_to='Category/', null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    # thinking of making this a many to many field
    catalog = models.ForeignKey(
        ProductCatalog, on_delete=models.SET_NULL, null=True, related_name="categories")

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.title


class Product(models.Model):

    product_id = models.UUIDField(
        default=uuid.uuid4, unique=True, blank=False, null=False, editable=False)

    name = models.CharField(max_length=250, unique=False)

    url_slug = models.SlugField()  # TODO: work on the slug field
    # this image field would later be given its own model for normalization

    image = models.ImageField(upload_to='products/', null=True, blank=True)

    brand = models.CharField(max_length=250)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField()
    # TODO: add another models for this field.
    long_description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    in_stock = models.PositiveIntegerField()
    active = models.BooleanField(default=False)
    # checks if the products is tangible or not
    digital = models.BooleanField(default=False)
    # thinking of how to implement the merchant
    merchant = models.OneToOneField(
        Merchant, blank=True, null=True, on_delete=models.CASCADE)
    # thinking of using a foreign key
    category = models.ManyToManyField(
        ProductCategory, related_name="products", blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class ProductQuestion(models.Model):
    # may be a CharField rather
    question = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='questions')
    # added this field to it to tell which customer posted the question
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Product Question'
        verbose_name_plural = 'Product Questions'

    def __str__(self):
        return f'{self.product.name} product questions'


class ProductAnswer(models.Model):

    answer = models.TextField()

    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE)

    # may be we should protect the answer when the customer is deleted
    # another model should be created to handle the voting
    voting = models.PositiveIntegerField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-updated',)
        verbose_name = 'Product Answer'
        verbose_name_plural = 'Product Answers'

    def __str__(self):
        return self.answer


class ProductReviews(models.Model):
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    # TODO: rating should be a new model
    rating = models.IntegerField(null=True)
    review = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    # I used models.PROTECT to prevent the review from being removed when customer is deleated
    # another thought when a customer is deleted it merchant account is deleted and its product is also deleted meaning protecting the productReveiw is not needed
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='reviews')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return f'{self.product.name} Reviews'
