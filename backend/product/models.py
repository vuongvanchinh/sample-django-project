from django.db import models
from core.fields import OrderField
from django.core.validators import MaxLengthValidator

# Create your models here.
class SeoModel(models.Model):
    seo_title = models.CharField(
        max_length=70, blank=True, null=True, validators=[MaxLengthValidator(70)]
    )
    seo_description = models.CharField(
        max_length=300, blank=True, null=True, validators=[MaxLengthValidator(300)]
    )

    class Meta:
        abstract = True


class Category(SeoModel):
    name = models.CharField(max_length=150, unique=True, null=False)
    description = models.TextField(blank=True, null=True)
    backgroundImage = models.ImageField(upload_to='category_background',null=True)
    parent = models.ForeignKey('self', related_name='childrens', on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    class Meta:
        ordering = ('name', )
    
    def __str__(self):
        return self.name
    
    def products(self):
        products = Product.objects.filter(category=self)
        for i in self.childrens:
            pass
        return products

class Product(SeoModel):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    weight = models.IntegerField(default=1) # unit is gam
    rating = models.FloatField(null=True, blank=True, default=0)
    
    publication_date = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

class ProductVariantCriterion(models.Model):
    product = models.ForeignKey(Product, related_name='criterions', on_delete=models.CASCADE)
    criterion_name = models.CharField(max_length=50)
    order = OrderField(blank=True, for_fields=['product'], null=True)
    def __str__(self):
        return f'{self.criterion_name} of {self.product.name}'

class ProductVariantOption(models.Model):
    criterion = models.ForeignKey(ProductVariantCriterion, related_name='options', on_delete=models.CASCADE, null=True)
    option_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.option_name} of {self.criterion.__str__()} id: {self.id}'

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)

    sku = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    combind_string = models.CharField(max_length=80) #red-m, red-l, green-m, green-l ...
    option_values = models.ManyToManyField(ProductVariantOption, related_name='variants')
    class Meta:
        ordering = ('sku','price')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images',
                            on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='product-images', blank=True, null=True)
    # order = OrderField(blank=True, for_fields=['product'])
    product_option_value = models.ForeignKey(
                                ProductVariantOption,
                                related_name='images',
                                on_delete=models.SET_NULL,
                                null=True)
    
