from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Category,
    Product,
    ProductVariant,
    ProductImage,
    Banner,
    Cart,
    CartItem,
    Order,
    OrderItem,
    PaymentProof,
    SiteSettings,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True, 'write_only': True, 'min_length': 6},
            'email': {'required': True},
        }

    def validate_email(self, value):
        """Validate that email is unique"""
        if not value:
            raise serializers.ValidationError("Email is required.")
        
        # Normalize email (lowercase)
        email = value.lower().strip()
        
        # Check if email already exists
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "An account with this email address already exists. Please use a different email or log in with your existing account."
            )
        return email

    def create(self, validated_data):
        email = validated_data.get('email', '').lower().strip()
        return User.objects.create_user(
            username=validated_data['username'],
            email=email,
            password=validated_data['password'],
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'image_url', 'variant', 'display_order', 'is_primary')
        read_only_fields = ('image_url',)
    
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            url = obj.image.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class ProductVariantSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_media = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ('id', 'size', 'color', 'stock', 'price', 'product_id', 'product_title', 'product_media', 'images')

    def get_price(self, obj):
        return float(obj.price)

    def get_product_media(self, obj):
        request = self.context.get('request')
        if obj.product.hero_media and hasattr(obj.product.hero_media, 'url'):
            url = obj.product.hero_media.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None
    
    def get_images(self, obj):
        # Get images for this specific variant (color)
        variant_images = obj.images.all()
        if variant_images.exists():
            return ProductImageSerializer(variant_images, many=True, context=self.context).data
        # Fallback to product images if no variant-specific images
        product_images = obj.product.images.filter(variant__isnull=True)
        if product_images.exists():
            return ProductImageSerializer(product_images, many=True, context=self.context).data
        return []


class ProductColorVariantSerializer(serializers.Serializer):
    """Serializer for displaying product color variants as separate items in listings"""
    product_id = serializers.IntegerField()
    title = serializers.CharField()
    color = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image_url = serializers.CharField(allow_null=True)
    category = CategorySerializer()
    slug = serializers.CharField()
    gender = serializers.CharField()
    has_stock = serializers.BooleanField()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    hero_media = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'category_id',
            'title',
            'slug',
            'description',
            'base_price',
            'gender',
            'hero_media',
            'is_featured',
            'is_active',
            'variants',
            'images',
            'created_at',
        )
        read_only_fields = ('slug', 'created_at')


class BannerSerializer(serializers.ModelSerializer):
    media_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Banner
        fields = '__all__'
        read_only_fields = ('created_at', 'media_url')
    
    def get_media_url(self, obj):
        if obj.media and hasattr(obj.media, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.media.url)
            return obj.media.url
        return None


class CartItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(), source='variant', write_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'variant', 'variant_id', 'quantity', 'subtotal')

    def get_subtotal(self, obj):
        return float(obj.subtotal)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_items', 'total_amount')

    def get_total_amount(self, obj):
        return float(obj.total_amount)


class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    product_image_url = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product_title',
            'size',
            'color',
            'price',
            'quantity',
            'product_image_url',
        )

    def get_price(self, obj):
        return float(obj.price)

    def get_product_image_url(self, obj):
        """Get product image from variant or product"""
        request = self.context.get('request')
        
        # Try to get image from variant if it exists
        if obj.variant:
            # Try variant-specific images first
            variant_images = obj.variant.images.all()
            if variant_images.exists():
                first_image = variant_images.first()
                if first_image.image and hasattr(first_image.image, 'url'):
                    url = first_image.image.url
                    if request:
                        return request.build_absolute_uri(url)
                    return url
            
            # Try product hero image
            if obj.variant.product.hero_media and hasattr(obj.variant.product.hero_media, 'url'):
                url = obj.variant.product.hero_media.url
                if request:
                    return request.build_absolute_uri(url)
                return url
            
            # Try product images (not linked to specific variant)
            product_images = obj.variant.product.images.filter(variant__isnull=True)
            if product_images.exists():
                first_image = product_images.first()
                if first_image.image and hasattr(first_image.image, 'url'):
                    url = first_image.image.url
                    if request:
                        return request.build_absolute_uri(url)
                    return url
        
        return None


class PaymentProofSerializer(serializers.ModelSerializer):
    proof_file_url = serializers.SerializerMethodField()

    class Meta:
        model = PaymentProof
        fields = ('id', 'reference_id', 'proof_file', 'proof_file_url', 'notes', 'verified', 'created_at')

    def get_proof_file_url(self, obj):
        if obj.proof_file and hasattr(obj.proof_file, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.proof_file.url)
            return obj.proof_file.url
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_amount = serializers.SerializerMethodField()
    payment_proof = PaymentProofSerializer(read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'status',
            'status_display',
            'shipping_address',
            'name',
            'email',
            'phone_number',
            'pin_code',
            'street_name',
            'city_town',
            'district',
            'address',
            'total_amount',
            'upi_reference',
            'payment_verified',
            'created_at',
            'items',
            'payment_proof',
            'user',
        )

    def get_total_amount(self, obj):
        return float(obj.total_amount)

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
        }


class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(required=False)  # Kept for backward compatibility
    # Separate address fields (all mandatory)
    name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True, max_length=20)
    pin_code = serializers.CharField(required=True, max_length=10)
    street_name = serializers.CharField(required=True, max_length=200)
    city_town = serializers.CharField(required=True, max_length=100)
    district = serializers.CharField(required=True, max_length=100)
    address = serializers.CharField(required=True)  # Full address field


class PaymentProofSerializer(serializers.ModelSerializer):
    proof_file_url = serializers.SerializerMethodField()

    class Meta:
        model = PaymentProof
        fields = '__all__'
        read_only_fields = ('verified',)

    def get_proof_file_url(self, obj):
        if obj.proof_file and hasattr(obj.proof_file, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.proof_file.url)
            return obj.proof_file.url
        return None


class SiteSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    homepage_banner_url = serializers.SerializerMethodField()
    qr_code_image_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = '__all__'

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None

    def get_homepage_banner_url(self, obj):
        request = self.context.get('request')
        if obj.homepage_banner and hasattr(obj.homepage_banner, 'url'):
            if request:
                return request.build_absolute_uri(obj.homepage_banner.url)
            return obj.homepage_banner.url
        return None

    def get_qr_code_image_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code_image and hasattr(obj.qr_code_image, 'url'):
            if request:
                return request.build_absolute_uri(obj.qr_code_image.url)
            return obj.qr_code_image.url
        return None

