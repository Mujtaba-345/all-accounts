from django.contrib import admin
from .models import Brand, Shop, Lager


class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created_at", "updated_at")


class ShopAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name", "brand", "created_at", "updated_at")


class LagerAdmin(admin.ModelAdmin):
    search_fields = ("shop__name",)
    list_display = ("id", "shop", "credit", "debit", "opening_balance", "created_at", "updated_at")


admin.site.register(Brand, BrandAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Lager, LagerAdmin)
