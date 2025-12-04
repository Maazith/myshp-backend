from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib import messages
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
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

# Customize admin site
admin.site.site_header = "EdithCloths Admin"
admin.site.site_title = "EdithCloths Admin"
admin.site.index_title = "Welcome to EdithCloths Administration"


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    can_delete = True
    verbose_name = "Variant"
    verbose_name_plural = "Variants (Optional - default variant is auto-created)"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'gender', 'base_price', 'is_active', 'variant_count')
    list_filter = ('gender', 'category', 'is_active')
    search_fields = ('title', 'description')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'description', 'base_price', 'gender')
        }),
        ('Media', {
            'fields': ('hero_media',)
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
    )
    inlines = [ProductVariantInline]  # Still allow editing variants, but not required

    def variant_count(self, obj):
        return obj.variants.count()
    variant_count.short_description = 'Variants'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('website_name', 'contact_email', 'contact_phone', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('website_name', 'logo', 'homepage_banner', 'about_text')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address', 'whatsapp_number', 'instagram_link')
        }),
        ('Payment Settings', {
            'fields': ('upi_id', 'qr_code_image')
        }),
    )
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        # Redirect to change form if settings exist
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        settings = SiteSettings.load()
        if settings.pk:
            return HttpResponseRedirect(reverse('admin:shop_sitesettings_change', args=[settings.pk]))
        return super().changelist_view(request, extra_context)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_amount', 'created_at')
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_title', 'size', 'color', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_amount', 'payment_verified', 'created_at')
    list_filter = ('status', 'payment_verified', 'created_at')
    search_fields = ('order_number', 'user__username', 'user__email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    actions = ['verify_payment']

    def verify_payment(self, request, queryset):
        for order in queryset:
            order.payment_verified = True
            order.status = 'PAYMENT_VERIFIED'
            order.save()
            if hasattr(order, 'payment_proof'):
                order.payment_proof.verified = True
                order.payment_proof.save()
        self.message_user(request, f"Payment verified for {queryset.count()} order(s).")
    verify_payment.short_description = "Verify payment for selected orders"


admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(Banner)
admin.site.register(OrderItem)
admin.site.register(PaymentProof)


# Custom Admin Dashboard
def dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('admin:index')

    # Calculate statistics
    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='DELIVERED').count()
    pending_orders = Order.objects.filter(
        Q(status='PLACED') | Q(status='PAYMENT_PENDING') | Q(status='PAYMENT_VERIFIED')
    ).count()
    cancelled_orders = Order.objects.filter(status='CANCELLED').count()
    total_users = User.objects.count()
    total_revenue = Order.objects.filter(
        payment_verified=True
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]

    # Order status breakdown
    status_breakdown = Order.objects.values('status').annotate(count=Count('id'))

    # Revenue by month (last 6 months)
    monthly_revenue = []
    for i in range(5, -1, -1):
        month = timezone.now() - timedelta(days=30 * i)
        month_start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        revenue = Order.objects.filter(
            payment_verified=True,
            created_at__gte=month_start,
            created_at__lt=next_month
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        monthly_revenue.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': float(revenue)
        })

    context = {
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'cancelled_orders': cancelled_orders,
        'total_users': total_users,
        'total_revenue': float(total_revenue),
        'recent_orders': recent_orders,
        'status_breakdown': status_breakdown,
        'monthly_revenue': monthly_revenue,
    }
    return render(request, 'admin/dashboard.html', context)
