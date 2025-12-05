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
    description = models.TextField(blank=True, default='')
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
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Auto-create default variant if no variants exist
        if is_new and not self.variants.exists():
            ProductVariant.objects.create(
                product=self,
                size='M',
                color='Black',
                stock=0
            )

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


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    variant = models.ForeignKey('ProductVariant', related_name='images', on_delete=models.CASCADE, null=True, blank=True, help_text="Link image to specific color variant")
    image = models.FileField(upload_to='products/images/')
    display_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['display_order', 'created_at']

    def __str__(self):
        variant_info = f" ({self.variant.color})" if self.variant else ""
        return f"{self.product.title}{variant_info} - Image {self.display_order}"


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
        ('PLACED', 'Placed'),
        ('PAYMENT_PENDING', 'Payment Pending'),
        ('PAYMENT_VERIFIED', 'Payment Verified'),
        ('SHIPPED', 'Shipped'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLACED')
    shipping_address = models.TextField()  # Kept for backward compatibility
    # Separate address fields
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)
    street_name = models.CharField(max_length=200, blank=True)
    city_town = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)  # Full address field
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    upi_reference = models.CharField(max_length=100, blank=True)
    payment_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4()).split('-')[0].upper()
        # Auto-set status based on payment verification
        if not self.payment_verified and self.status == 'PLACED':
            self.status = 'PAYMENT_PENDING'
        elif self.payment_verified and self.status == 'PAYMENT_PENDING':
            self.status = 'PAYMENT_VERIFIED'
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


class SiteSettings(models.Model):
    """Singleton model for site-wide settings"""
    website_name = models.CharField(max_length=200, default='EdithCloths')
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    homepage_banner = models.ImageField(upload_to='settings/', blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, default='')
    qr_code_image = models.ImageField(upload_to='settings/', blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, default='')
    contact_email = models.EmailField(blank=True, default='')
    contact_address = models.TextField(blank=True, default='')
    about_text = models.TextField(blank=True, default='')
    whatsapp_number = models.CharField(max_length=20, blank=True, default='', help_text='WhatsApp number for customer support')
    instagram_link = models.CharField(max_length=100, blank=True, default='', help_text='Instagram username or profile link')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Site Settings'
