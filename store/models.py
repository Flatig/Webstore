from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


def product_image_upload(instance, filename):
    return 'product_image/{0}/{1}'.format(instance.name, filename)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to=product_image_upload, blank=True, default='static/images/no_image.jpg')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # Image check
    def get_image(self):  # Use in templates
        return self.image.url if self.image and self.image.storage.exists(
            self.image.name) else '/static/images/no_image.jpg'
