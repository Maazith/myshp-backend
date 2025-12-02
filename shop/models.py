from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid
from decimal import Decimal


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True)
    hero_media = models.FileField(upload_to='categories/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    class Gender(models.TextChoices):
        MEN = 'MEN', 'Men'
        WOMEN = 'WOMEN', 'Women'
        UNISEX = 'UNISEX', 'Unisex'

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.UNISEX)
    hero_media = models.FileField(upload_to='products/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductVariant(TimeStampedModel):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ('product', 'size', 'color')

    def __str__(self):
        return f"{self.product.title} - {self.size}/{self.color}"

    @property
    def price(self):
        return self.price_override or self.product.base_price


class Banner(TimeStampedModel):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, blank=True)
    media = models.FileField(upload_to='banners/')
    cta_text = models.CharField(max_length=50, blank=True)
    cta_link = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title


class Cart(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='cart', on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart {self.pk} - {self.user}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_amount(self):
        total = sum(
            (Decimal(str(item.subtotal)) for item in self.items.select_related('variant', 'variant__product')),
            Decimal('0.00'),
        )
        return total


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'variant')

    def __str__(self):
        return f"{self.variant} x {self.quantity}"

    @property
    def subtotal(self):
        return Decimal(self.variant.price) * self.quantity


class Order(TimeStampedModel):
    STATUS_CHOICES = [
        ('PLACED', 'Order Placed'),
        ('SHIPPED', 'Shipped'),
        ('REACHED', 'Reached Local Transport Office'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLACED')
    shipping_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    upi_reference = models.CharField(max_length=100, blank=True)
    payment_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4()).split('-')[0].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    product_title = models.CharField(max_length=200)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_title} ({self.order.order_number})"


class PaymentProof(TimeStampedModel):
    order = models.OneToOneField(Order, related_name='payment_proof', on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=100)
    proof_file = models.FileField(upload_to='payments/', blank=True, null=True)
    notes = models.TextField(blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"PaymentProof #{self.order.order_number}"

# Create your models here.
