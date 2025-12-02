from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Category,
    Product,
    ProductVariant,
    Banner,
    Cart,
    CartItem,
    Order,
    OrderItem,
    PaymentProof,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_media = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ('id', 'size', 'color', 'stock', 'price', 'product_id', 'product_title', 'product_media')

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


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    variants = ProductVariantSerializer(many=True, read_only=True)
    base_price = serializers.SerializerMethodField()
    hero_media = serializers.SerializerMethodField()

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
            'created_at',
        )

    def get_base_price(self, obj):
        return float(obj.base_price)

    def get_hero_media(self, obj):
        if obj.hero_media and hasattr(obj.hero_media, 'url'):
            request = self.context.get('request')
            url = obj.hero_media.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


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

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product_title',
            'size',
            'color',
            'price',
            'quantity',
        )

    def get_price(self, obj):
        return float(obj.price)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'status',
            'status_display',
            'shipping_address',
            'total_amount',
            'upi_reference',
            'payment_verified',
            'created_at',
            'items',
        )

    def get_total_amount(self, obj):
        return float(obj.total_amount)


class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()


class PaymentProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProof
        fields = '__all__'
        read_only_fields = ('verified',)

