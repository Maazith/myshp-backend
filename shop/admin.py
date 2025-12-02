from django.contrib import admin
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


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'gender', 'base_price', 'is_active')
    list_filter = ('gender', 'category', 'is_active')
    search_fields = ('title', 'description')
    inlines = [ProductVariantInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(ProductVariant)
admin.site.register(Banner)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentProof)
