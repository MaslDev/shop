from django.db import models
from django.urls import reverse
import datetime
from django.db.models.signals import post_save
import mptt
from mptt.models import MPTTModel, TreeForeignKey
from authentication.user import User


class Category(MPTTModel):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Category', unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # slug = models.SlugField(max_length=200, db_index=True, unique=True, null=True, blank=True)
    # url = models.CharField(max_length=255, null=True)

    def get_products(self):
        return self.products.all()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        # unique_together = ('slug', 'parent',)

    def __str__(self):
        return self.name

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']


        # def save(self, *args, **kwargs):
        #     if self.slug is None:
        #         # create a slug that unique to siblings
        #         slug = slugify(self.name)
        #         self.slug = slug
        #         siblings = self.get_siblings()
        #         i = 1
        #         while siblings.filter(slug=self.slug).exists():
        #             i += 1
        #             self.slug = slug + '-%d' % i
        #
        #         # now create a URL based on parent url + slug
        #         if self.parent:
        #             self.url = '%s/%s' % (self.parent.url, self.slug)
        #         else:
        #             self.url = self.slug
        #     super(Category, self).save(*args, **kwargs)


mptt.register(Category, order_insertion_by=['name'])


class Product(models.Model):
    category = TreeForeignKey(Category, related_name='products', verbose_name="Category", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True, verbose_name="Name")
    # slug = models.SlugField(max_length=200, db_index=True)
    main_image = models.ImageField(upload_to='products/images/mainImage/%Y/%m/%d', blank=True, null=True)
    short_description = models.CharField(max_length=200, blank=True, verbose_name="Short description")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.PositiveIntegerField(verbose_name="Stock")
    available = models.BooleanField(default=True, verbose_name="Available")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        # index_together = [
        #     ['id', 'slug']
        # ]

    def __str__(self):
        return self.name

        # def get_absolute_url(self):
        #     return reverse('okna:ProductDetail', args=[self.id, self.slug])


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")

    class Meta:
        verbose_name = 'Cart Item'


# class Comment(models.Model):
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField('Comment')
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
#     pub_date = models.DateTimeField('Comment date', default=datetime.datetime.now)
#
#     class Meta:
#         ordering = ['pub_date']
#
#     class MPTTMeta:
#         order_insertion_by = ['pub_date']
#
#
# mptt.register(Comment, order_insertion_by=['pub_date'])


class ProductImages(models.Model):
    product = models.ForeignKey(Product, default=None, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/%Y/%m/%d', blank=True, null=True)
