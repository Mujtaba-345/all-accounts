from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from utils.common import BaseTimestampModel


class Brand(BaseTimestampModel):
    name = models.CharField(_("Name"), max_length=70)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_brand")

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Shop(BaseTimestampModel):
    name = models.CharField(_("Name"), max_length=70)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brands')

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Lager(BaseTimestampModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shops')
    credit = models.CharField(_("Credit"), max_length=70)
    debit = models.CharField(_("Debit"), max_length=70)
    opening_balance = models.CharField(_("Opening Balance"), max_length=70)

    class Meta:
        verbose_name = "Lager"
        verbose_name_plural = "Lagers"
        ordering = ["-id"]

    def __str__(self):
        return self.shop.name
