from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

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
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ProductSerializer,
    CategorySerializer,
    BannerSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    CheckoutSerializer,
    PaymentProofSerializer,
)


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            username = request.data.get('username') or request.data.get('email')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
            response.data['user'] = UserSerializer(user).data if user else None
        return response


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ProductListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        gender = request.query_params.get('gender')
        queryset = Product.objects.filter(is_active=True)
        if gender in dict(Product.Gender.choices):
            queryset = queryset.filter(gender=gender)
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        self._sync_variants(product, request.data.get('variants'))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _sync_variants(self, product, variants_raw):
        if not variants_raw:
            return
        try:
            variants = json.loads(variants_raw) if isinstance(variants_raw, str) else variants_raw
        except json.JSONDecodeError:
            return
        ProductVariant.objects.filter(product=product).delete()
        for variant in variants:
            ProductVariant.objects.create(
                product=product,
                size=variant.get('size', 'M'),
                color=variant.get('color', 'Black'),
                stock=variant.get('stock', 0),
                price_override=variant.get('price'),
            )


class ProductUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        variants = request.data.get('variants')
        if variants is not None:
            ProductVariant.objects.filter(product=product).delete()
            try:
                payload = json.loads(variants) if isinstance(variants, str) else variants
            except json.JSONDecodeError:
                payload = []
            for variant in payload:
                ProductVariant.objects.create(
                    product=product,
                    size=variant.get('size', 'M'),
                    color=variant.get('color', 'Black'),
                    stock=variant.get('stock', 0),
                    price_override=variant.get('price'),
                )
        return Response(serializer.data)


class ProductDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data)


class CategoryCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BannerListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = BannerSerializer(Banner.objects.filter(is_active=True), many=True)
        return Response(serializer.data)


class BannerUploadView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = BannerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BannerDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        banner = get_object_or_404(Banner, pk=pk)
        banner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = get_user_cart(request.user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)


class CartAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_user_cart(request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        variant = serializer.validated_data['variant']
        quantity = serializer.validated_data['quantity']
        item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
        item.quantity = quantity if created else item.quantity + quantity
        item.save()
        return Response(CartSerializer(cart, context={'request': request}).data, status=status.HTTP_201_CREATED)


class CartUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        cart = get_user_cart(request.user)
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity', 1))
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        item.quantity = max(quantity, 1)
        item.save()
        return Response(CartSerializer(cart, context={'request': request}).data)


class CartRemoveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        cart = get_user_cart(request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        item.delete()
        return Response(CartSerializer(cart, context={'request': request}).data)


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_user_cart(request.user)
        if not cart.items.exists():
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.create(
            user=request.user,
            shipping_address=serializer.validated_data['shipping_address'],
            total_amount=cart.total_amount,
        )
        for item in cart.items.select_related('variant', 'variant__product'):
            OrderItem.objects.create(
                order=order,
                variant=item.variant,
                product_title=item.variant.product.title,
                size=item.variant.size,
                color=item.variant.color,
                price=item.variant.price,
                quantity=item.quantity,
            )
            item.variant.stock = max(item.variant.stock - item.quantity, 0)
            item.variant.save()
        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class ConfirmPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PaymentProofSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = get_object_or_404(Order, pk=serializer.validated_data['order'].id, user=request.user)
        order.upi_reference = serializer.validated_data['reference_id']
        order.save()
        proof, _ = PaymentProof.objects.update_or_create(
            order=order,
            defaults={
                'reference_id': serializer.validated_data['reference_id'],
                'proof_file': serializer.validated_data.get('proof_file'),
                'notes': serializer.validated_data.get('notes', ''),
            },
        )
        return Response(OrderSerializer(order).data)


class MyOrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class AdminOrdersView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class AdminMarkPaidView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.payment_verified = True
        order.save()
        if hasattr(order, 'payment_proof'):
            proof = order.payment_proof
            proof.verified = True
            proof.save()
        return Response(OrderSerializer(order).data)


class AdminOrderStatusView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        status_value = request.data.get('status')
        if status_value not in dict(Order.STATUS_CHOICES):
            return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=pk)
        order.status = status_value
        order.save()
        return Response(OrderSerializer(order).data)
