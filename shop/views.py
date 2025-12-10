from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import json
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes

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
from .utils import send_order_notification_to_admin, send_order_confirmation_to_user
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
    SiteSettingsSerializer,
)


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def get_or_create_session_user(request):
    """Get or create an anonymous user for session-based cart"""
    if request.user.is_authenticated:
        return request.user
    
    # Ensure session is created
    if not request.session.session_key:
        request.session.create()
    
    # Check if we have a session user ID
    session_user_id = request.session.get('anonymous_user_id')
    if session_user_id:
        try:
            user = User.objects.get(pk=session_user_id)
            return user
        except User.DoesNotExist:
            # Session user was deleted, create a new one
            pass
    
    # Create a new anonymous user
    # Use session key if available, otherwise use timestamp
    if request.session.session_key:
        session_key_part = request.session.session_key[:8] if len(request.session.session_key) >= 8 else request.session.session_key
    else:
        import time
        session_key_part = str(int(time.time()))[-8:]
    
    username = f'anonymous_{session_key_part}'
    # Ensure username is unique
    counter = 1
    original_username = username
    while User.objects.filter(username=username).exists():
        username = f'{original_username}_{counter}'
        counter += 1
    
    try:
        user = User.objects.create_user(
            username=username,
            email=f'{username}@anonymous.local',
            is_active=False  # Mark as inactive since it's anonymous
        )
        request.session['anonymous_user_id'] = user.id
        request.session.save()  # Explicitly save the session
        return user
    except Exception as e:
        # Fallback: try to get or create with a simpler approach
        import uuid
        username = f'anonymous_{uuid.uuid4().hex[:8]}'
        user = User.objects.create_user(
            username=username,
            email=f'{username}@anonymous.local',
            is_active=False
        )
        request.session['anonymous_user_id'] = user.id
        request.session.save()
        return user


class APIRootView(APIView):
    """API root endpoint - shows available endpoints"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'message': 'EdithCloths API',
            'version': '1.0',
            'endpoints': {
                'auth': '/api/auth/register, /api/auth/login, /api/auth/refresh, /api/auth/me',
                'products': '/api/products/',
                'categories': '/api/categories/',
                'banners': '/api/banners/',
                'cart': '/api/cart/',
                'orders': '/api/orders/',
                'settings': '/api/settings/',
            },
            'status': 'online'
        })


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            # Format validation errors for better user experience
            errors = {}
            for field, messages in serializer.errors.items():
                if isinstance(messages, list):
                    errors[field] = messages[0] if messages else 'Invalid value'
                else:
                    errors[field] = str(messages)
            
            # Return user-friendly error message
            error_message = 'Registration failed. '
            if 'email' in errors:
                error_message += errors['email']
            elif 'username' in errors:
                error_message += errors['username']
            elif 'password' in errors:
                error_message += errors['password']
            else:
                error_message += 'Please check your input and try again.'
            
            return Response(
                {'detail': error_message, 'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                username = request.data.get('username') or request.data.get('email')
                if username:
                    try:
                        user = User.objects.get(username=username)
                        response.data['user'] = UserSerializer(user).data
                    except User.DoesNotExist:
                        # User doesn't exist - this shouldn't happen if login succeeded
                        # But handle gracefully
                        response.data['user'] = None
                else:
                    response.data['user'] = None
            return response
        except Exception as e:
            # Handle authentication errors more gracefully
            error_message = 'Invalid username or password. Please check your credentials and try again.'
            
            # Log error for debugging (but don't expose to client)
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Login error: {str(e)}")
            
            return Response(
                {
                    'detail': error_message
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ProductListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        gender = request.query_params.get('gender')
        expand_by_color = request.query_params.get('expand_by_color', 'false').lower() == 'true'
        
        queryset = Product.objects.filter(is_active=True).prefetch_related('variants', 'variants__images', 'images', 'category')
        if gender in dict(Product.Gender.choices):
            # Include products with matching gender OR UNISEX products
            queryset = queryset.filter(
                Q(gender=gender) | Q(gender=Product.Gender.UNISEX)
            )
        
        # If expand_by_color is true, return one entry per color variant
        if expand_by_color:
            expanded_products = []
            for product in queryset:
                # Get all unique colors for this product
                unique_colors = product.variants.values_list('color', flat=True).distinct()
                
                if not unique_colors:
                    # No variants, show product as-is with base price
                    expanded_products.append({
                        'product_id': product.id,
                        'title': product.title,
                        'color': None,
                        'price': float(product.base_price),
                        'image_url': self._get_product_image_url(product, request),
                        'category': {
                            'id': product.category.id,
                            'name': product.category.name,
                            'slug': product.category.slug,
                        },
                        'slug': product.slug,
                        'gender': product.gender,
                        'has_stock': False,
                    })
                else:
                    # Create one entry per color
                    for color in unique_colors:
                        # Get first variant with this color to determine price
                        color_variant = product.variants.filter(color=color).first()
                        price = float(color_variant.price) if color_variant else float(product.base_price)
                        
                        # Check if any variant of this color has stock
                        has_stock = product.variants.filter(color=color, stock__gt=0).exists()
                        
                        # Get image for this color variant
                        image_url = self._get_color_image_url(product, color, request)
                        
                        expanded_products.append({
                            'product_id': product.id,
                            'title': f"{product.title} - {color}",
                            'base_title': product.title,  # Keep original title
                            'color': color,
                            'price': price,
                            'image_url': image_url,
                            'category': {
                                'id': product.category.id,
                                'name': product.category.name,
                                'slug': product.category.slug,
                            },
                            'slug': product.slug,
                            'gender': product.gender,
                            'has_stock': has_stock,
                        })
            
            # Debug logging
            print(f"📦 Expanded products by color - Gender filter: {gender}, Total color variants: {len(expanded_products)}")
            return Response(expanded_products)
        else:
            # Original behavior - return products as-is
            serializer = ProductSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
    
    def _get_product_image_url(self, product, request):
        """Get product hero image or first product image"""
        if product.hero_media and hasattr(product.hero_media, 'url'):
            url = product.hero_media.url
            if request:
                return request.build_absolute_uri(url)
            return url
        
        # Try product images (not linked to specific variant)
        first_image = product.images.filter(variant__isnull=True).first()
        if first_image and first_image.image and hasattr(first_image.image, 'url'):
            url = first_image.image.url
            if request:
                return request.build_absolute_uri(url)
            return url
        
        # Try first variant image if no product-level images
        if product.variants.exists():
            first_variant = product.variants.first()
            variant_image = ProductImage.objects.filter(variant=first_variant, is_primary=True).first() or \
                           ProductImage.objects.filter(variant=first_variant).first()
            if variant_image and variant_image.image and hasattr(variant_image.image, 'url'):
                url = variant_image.image.url
                if request:
                    return request.build_absolute_uri(url)
                return url
        
        return None
    
    def _get_color_image_url(self, product, color, request):
        """Get first image for a specific color variant"""
        # Try to find variant-specific images
        variant = product.variants.filter(color=color).first()
        if variant:
            # Get ProductImage objects linked to this variant
            variant_image = ProductImage.objects.filter(variant=variant, is_primary=True).first() or \
                           ProductImage.objects.filter(variant=variant).first()
            if variant_image and variant_image.image and hasattr(variant_image.image, 'url'):
                url = variant_image.image.url
                if request:
                    return request.build_absolute_uri(url)
                return url
        
        # Fallback to product hero image or first product image
        return self._get_product_image_url(product, request)


class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_active=True)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)


class ProductDetailByIdView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        # Allow admin to see inactive products
        if request.user.is_staff:
            product = get_object_or_404(Product, pk=pk)
        else:
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
        try:
            # Validate required fields
            if not request.data.get('title'):
                return Response(
                    {'detail': 'Product title is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not request.data.get('category_id'):
                return Response(
                    {'detail': 'Category is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Base price is optional - will be calculated from variants if not provided
            base_price = request.data.get('base_price', 0)
            if not base_price or float(base_price) == 0:
                # Will be set from variant prices after variants are created
                base_price = 0
            
            serializer = ProductSerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                # Format validation errors better
                errors = {}
                for field, messages in serializer.errors.items():
                    if isinstance(messages, list):
                        errors[field] = messages[0] if messages else 'Invalid value'
                    else:
                        errors[field] = str(messages)
                return Response(
                    {'detail': errors if len(errors) > 1 else list(errors.values())[0]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            product = serializer.save()
            
            # Sync variants first (they contain price information)
            created_variants_dict = self._sync_variants(product, request.data.get('variants'))
            
            # Calculate base_price from first variant if not set
            if not product.base_price or product.base_price == 0:
                # Get first variant from created variants
                first_variant = None
                if created_variants_dict:
                    # created_variants_dict is a dict by color, get first variant
                    for color, variants_list in created_variants_dict.items():
                        if variants_list:
                            first_variant = variants_list[0]
                            break
                
                if first_variant:
                    # Get price from first variant (use price_override or product.base_price)
                    calculated_price = float(first_variant.price)
                    if calculated_price > 0:
                        product.base_price = calculated_price
                        product.save(update_fields=['base_price'])
            
            # Ensure product is active
            if not product.is_active:
                product.is_active = True
                product.save()
            
            self._sync_variant_images(product, request.FILES)
            # Return full product data
            product_data = ProductSerializer(product, context={'request': request}).data
            print(f"✅ Product created: {product.title} (ID: {product.id}, Gender: {product.gender}, Active: {product.is_active})")
            return Response(product_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            error_detail = str(e)
            if settings.DEBUG:
                error_detail += f'\n\nTraceback:\n{traceback.format_exc()}'
            return Response(
                {'detail': f'Error creating product: {error_detail}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _sync_variants(self, product, variants_raw):
        if not variants_raw:
            # Auto-create default variant if none provided
            default_variant = None
            if not product.variants.exists():
                default_variant = ProductVariant.objects.create(
                    product=product,
                    size='M',
                    color='Black',
                    stock=0
                )
            if default_variant:
                return {'Black': [default_variant]}
            return {}
        try:
            variants = json.loads(variants_raw) if isinstance(variants_raw, str) else variants_raw
        except json.JSONDecodeError:
            # If JSON is invalid, create default variant
            if not product.variants.exists():
                ProductVariant.objects.create(
                    product=product,
                    size='M',
                    color='Black',
                    stock=0
                )
            return
        
        # Delete existing variants and their images
        # Delete images first to avoid foreign key constraint issues
        try:
            ProductImage.objects.filter(product=product).delete()
        except Exception as e:
            # Table might not exist yet or other error - log and continue
            print(f"Note: Could not delete ProductImage records: {e}")
        
        # Now delete variants
        ProductVariant.objects.filter(product=product).delete()
        
        # Create new variants
        created_variants = {}
        for variant in variants:
            color = variant.get('color', 'Black')
            size = variant.get('size', 'M')
            stock = variant.get('stock', 0)
            price_override = variant.get('price')  # Price override per color
            if price_override:
                try:
                    price_override = float(price_override)
                except (ValueError, TypeError):
                    price_override = None
            
            variant_obj, created = ProductVariant.objects.get_or_create(
                product=product,
                size=size,
                color=color,
                defaults={
                    'stock': stock,
                    'price_override': price_override
                }
            )
            if not created:
                variant_obj.stock = stock
                if price_override:
                    variant_obj.price_override = price_override
                variant_obj.save()
            
            # Store variant by color for image linking
            if color not in created_variants:
                created_variants[color] = []
            created_variants[color].append(variant_obj)
        
        return created_variants
    
    def _sync_variant_images(self, product, files):
        """Process and link images to variants based on FormData keys"""
        if not files:
            return
        
        # Process variant images (format: variant_{idx}_color_{color}_image_{imgIdx})
        variant_images_map = {}
        
        for key, file in files.items():
            if key.startswith('variant_') and '_color_' in key:
                # Parse: variant_{idx}_color_{color}_image_{imgIdx}
                parts = key.split('_')
                try:
                    color_idx = parts.index('color')
                    color = parts[color_idx + 1]
                    
                    if color not in variant_images_map:
                        variant_images_map[color] = []
                    variant_images_map[color].append(file)
                except (IndexError, ValueError):
                    continue
        
        # Link images to variants
        for color, images in variant_images_map.items():
            # Find variants with this color
            variants = ProductVariant.objects.filter(product=product, color=color)
            if variants.exists():
                variant = variants.first()  # Use first variant of this color
                for idx, image_file in enumerate(images):
                    try:
                        ProductImage.objects.create(
                            product=product,
                            variant=variant,
                            image=image_file,
                            display_order=idx,
                            is_primary=(idx == 0)
                        )
                    except Exception as e:
                        print(f"Error creating ProductImage: {e}")
                        # Continue with other images even if one fails


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
        try:
            product = get_object_or_404(Product, pk=pk)
            product_title = product.title
            # Delete related objects first (variants, images, etc.)
            product.variants.all().delete()
            if hasattr(product, 'images'):
                product.images.all().delete()
            product.delete()
            print(f"✅ Product deleted: {product_title} (ID: {pk})")
            return Response({'detail': 'Product deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            error_detail = str(e)
            if settings.DEBUG:
                error_detail += f'\n\nTraceback:\n{traceback.format_exc()}'
            print(f"❌ Error deleting product: {error_detail}")
            return Response(
                {'detail': f'Error deleting product: {error_detail}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        serializer = BannerSerializer(Banner.objects.filter(is_active=True), many=True, context={'request': request})
        return Response(serializer.data)


class BannerUploadView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        try:
            # Check if file is present
            if 'media' not in request.FILES:
                return Response(
                    {'detail': 'Banner image file is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate file type
            uploaded_file = request.FILES['media']
            allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
            if uploaded_file.content_type not in allowed_types:
                return Response(
                    {'detail': f'Invalid file type: {uploaded_file.content_type}. Allowed types: PNG, JPG, JPEG, GIF, WEBP'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate file size (max 10MB)
            max_size = 10 * 1024 * 1024  # 10MB
            if uploaded_file.size > max_size:
                return Response(
                    {'detail': f'File size too large: {uploaded_file.size} bytes. Maximum size is 10MB'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = BannerSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            banner = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'detail': f'Error uploading banner: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BannerDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        banner = get_object_or_404(Banner, pk=pk)
        banner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminBulkDeleteView(APIView):
    """Bulk delete all products or banners"""
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request):
        delete_type = request.data.get('type')  # 'products' or 'banners'
        
        if delete_type == 'products':
            products = Product.objects.all()
            count = products.count()
            # Delete all products (cascades will delete variants, images, etc.)
            products.delete()
            return Response({
                'detail': f'Successfully deleted {count} product(s)',
                'deleted_count': count
            }, status=status.HTTP_200_OK)
        
        elif delete_type == 'banners':
            banners = Banner.objects.all()
            count = banners.count()
            banners.delete()
            return Response({
                'detail': f'Successfully deleted {count} banner(s)',
                'deleted_count': count
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                'detail': 'Invalid type. Use "products" or "banners"'
            }, status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = get_or_create_session_user(request)
        cart = get_user_cart(user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)


class CartAddView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = get_or_create_session_user(request)
        cart = get_user_cart(user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        variant = serializer.validated_data['variant']
        quantity = serializer.validated_data['quantity']
        item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
        item.quantity = quantity if created else item.quantity + quantity
        item.save()
        return Response(CartSerializer(cart, context={'request': request}).data, status=status.HTTP_201_CREATED)


class CartUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request):
        user = get_or_create_session_user(request)
        cart = get_user_cart(user)
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity', 1))
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        item.quantity = max(quantity, 1)
        item.save()
        return Response(CartSerializer(cart, context={'request': request}).data)


class CartRemoveView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, pk):
        user = get_or_create_session_user(request)
        cart = get_user_cart(user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        item.delete()
        return Response(CartSerializer(cart, context={'request': request}).data)


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # User must be authenticated (not anonymous)
        if not request.user.is_authenticated or not request.user.is_active:
            return Response(
                {'detail': 'Authentication required. Please log in to checkout.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Transfer cart from anonymous user if exists
        anonymous_user_id = request.session.get('anonymous_user_id')
        if anonymous_user_id:
            try:
                anonymous_user = User.objects.get(pk=anonymous_user_id, is_active=False)
                anonymous_cart = get_user_cart(anonymous_user)
                user_cart = get_user_cart(request.user)
                
                # Transfer cart items from anonymous to authenticated user
                for item in anonymous_cart.items.all():
                    existing_item = user_cart.items.filter(variant=item.variant).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                        existing_item.save()
                    else:
                        item.cart = user_cart
                        item.save()
                
                # Clear anonymous cart
                anonymous_cart.items.all().delete()
                # Remove anonymous user ID from session
                del request.session['anonymous_user_id']
            except User.DoesNotExist:
                pass
        
        user = request.user
        cart = get_user_cart(user)
        if not cart.items.exists():
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Build full shipping address from separate fields for backward compatibility
        validated_data = serializer.validated_data
        full_address = f"{validated_data.get('address', '')}\n{validated_data.get('street_name', '')}\n{validated_data.get('city_town', '')}, {validated_data.get('district', '')} - {validated_data.get('pin_code', '')}"
        
        order = Order.objects.create(
            user=user,
            shipping_address=validated_data.get('shipping_address', full_address),
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            pin_code=validated_data['pin_code'],
            street_name=validated_data['street_name'],
            city_town=validated_data['city_town'],
            district=validated_data['district'],
            address=validated_data['address'],
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
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = get_or_create_session_user(request)
        order_id = request.data.get('order')
        if isinstance(order_id, str):
            try:
                order_id = int(order_id)
            except ValueError:
                return Response({'detail': 'Invalid order ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = get_object_or_404(Order, pk=order_id, user=user)
        reference_id = request.data.get('reference_id', '')
        proof_file = request.FILES.get('proof_file')
        notes = request.data.get('notes', '')
        
        # Validate that screenshot is provided
        if not proof_file:
            return Response({'detail': 'Payment screenshot is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not reference_id:
            return Response({'detail': 'UPI Reference ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.upi_reference = reference_id
        order.status = 'PAYMENT_PENDING'  # Set status to payment pending
        order.save()
        
        proof, _ = PaymentProof.objects.update_or_create(
            order=order,
            defaults={
                'reference_id': reference_id,
                'proof_file': proof_file,
                'notes': notes,
            },
        )
        
        # Send email notification to admin
        send_order_notification_to_admin(order)
        
        return Response(OrderSerializer(order).data)


class MyOrdersView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = get_or_create_session_user(request)
        orders = Order.objects.filter(user=user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class AdminOrdersView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)


class AdminMarkPaidView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.payment_verified = True
        order.status = 'PLACED'  # Mark order as placed when admin approves
        order.save()
        if hasattr(order, 'payment_proof'):
            proof = order.payment_proof
            proof.verified = True
            proof.save()
        
        # Send confirmation email to user
        send_order_confirmation_to_user(order)
        
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


class SiteSettingsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsSerializer(settings, context={'request': request})
        return Response(serializer.data)


class SiteSettingsUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsSerializer(settings, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# User Authentication Views (Template-based)
@require_http_methods(["GET", "POST"])
def user_login_view(request):
    """User login page"""
    if request.user.is_authenticated:
        # Redirect to checkout if coming from checkout, otherwise home
        next_url = request.GET.get('next', '/')
        return redirect(next_url)
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        next_url = request.POST.get('next', request.GET.get('next', '/'))
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'shop/login.html', {'next': next_url})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Transfer cart from anonymous user if exists
            anonymous_user_id = request.session.get('anonymous_user_id')
            if anonymous_user_id:
                try:
                    anonymous_user = User.objects.get(pk=anonymous_user_id, is_active=False)
                    anonymous_cart = get_user_cart(anonymous_user)
                    user_cart = get_user_cart(user)
                    
                    # Transfer cart items
                    for item in anonymous_cart.items.all():
                        existing_item = user_cart.items.filter(variant=item.variant).first()
                        if existing_item:
                            existing_item.quantity += item.quantity
                            existing_item.save()
                        else:
                            item.cart = user_cart
                            item.save()
                    
                    anonymous_cart.items.all().delete()
                    del request.session['anonymous_user_id']
                except User.DoesNotExist:
                    pass
            
            # Generate JWT tokens for frontend API calls
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # If redirecting to frontend (checkout.html or any .html), include tokens in URL
            if next_url:
                # Check if it's a frontend URL (contains .html or is a full URL)
                if '.html' in next_url or next_url.startswith('http'):
                    # Add tokens as URL parameters
                    separator = '&' if '?' in next_url else '?'
                    redirect_url = f"{next_url}{separator}token={access_token}&refresh={refresh_token}"
                    return redirect(redirect_url)
                # If it's a relative path that might be frontend, try to construct full URL
                elif next_url.startswith('/') and 'checkout' in next_url:
                    # Assume frontend is on same domain or construct from request
                    # For now, just redirect with tokens in session (will be handled by frontend)
                    request.session['jwt_access_token'] = access_token
                    request.session['jwt_refresh_token'] = refresh_token
                    return redirect(next_url)
            
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    next_url = request.GET.get('next', '/')
    return render(request, 'shop/login.html', {'next': next_url})


@require_http_methods(["GET", "POST"])
def user_signup_view(request):
    """User signup page"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        next_url = request.POST.get('next', request.GET.get('next', '/'))
        
        # Validation
        errors = []
        if not username:
            errors.append('Username is required.')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists. Please choose another.')
        
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email__iexact=email).exists():
            errors.append('An account with this email already exists. Please log in instead.')
        
        if not password:
            errors.append('Password is required.')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        
        if password != password_confirm:
            errors.append('Passwords do not match.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'shop/signup.html', {'next': next_url})
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            
            # Transfer cart from anonymous user if exists
            anonymous_user_id = request.session.get('anonymous_user_id')
            if anonymous_user_id:
                try:
                    anonymous_user = User.objects.get(pk=anonymous_user_id, is_active=False)
                    anonymous_cart = get_user_cart(anonymous_user)
                    user_cart = get_user_cart(user)
                    
                    # Transfer cart items
                    for item in anonymous_cart.items.all():
                        existing_item = user_cart.items.filter(variant=item.variant).first()
                        if existing_item:
                            existing_item.quantity += item.quantity
                            existing_item.save()
                        else:
                            item.cart = user_cart
                            item.save()
                    
                    anonymous_cart.items.all().delete()
                    del request.session['anonymous_user_id']
                except User.DoesNotExist:
                    pass
            
            messages.success(request, 'Account created successfully!')
            
            # Generate JWT tokens for frontend API calls
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # If redirecting to frontend, include tokens in URL
            if next_url:
                if '.html' in next_url or next_url.startswith('http'):
                    separator = '&' if '?' in next_url else '?'
                    redirect_url = f"{next_url}{separator}token={access_token}&refresh={refresh_token}"
                    return redirect(redirect_url)
                elif next_url.startswith('/') and 'checkout' in next_url:
                    request.session['jwt_access_token'] = access_token
                    request.session['jwt_refresh_token'] = refresh_token
                    return redirect(next_url)
            
            return redirect('/')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    next_url = request.GET.get('next', '/')
    return render(request, 'shop/signup.html', {'next': next_url})


@login_required
def user_logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/')
