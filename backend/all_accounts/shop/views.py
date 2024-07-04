from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Brand, Shop, Lager
from django.views.generic import DeleteView
from django.urls import reverse_lazy


@method_decorator(login_required, name='dispatch')
class BrandView(View):
    def get(self, request, pk=None):
        user = request.user
        if pk:
            brand_obj = Brand.objects.filter(id=pk).first()
            return render(request, "shop/update_brands.html", {"brand_obj": brand_obj})
        else:
            brand_obj = Brand.objects.filter(user=user)
            context = {"brand_obj": brand_obj}
            return render(request, "shop/brands.html", context)

    def post(self, request, pk=None):
        if pk:
            brand_name = request.POST.get("brand_name")
            brand_obj = Brand.objects.get(id=pk)
            brand_obj.name = brand_name
            brand_obj.save()
            messages.success(request, "Brand Updated Successfully")
            return redirect("brands")
        else:
            user = request.user
            brand_name = request.POST.get("brand_name")
            Brand.objects.create(name=brand_name, user=user)
            messages.success(request, "Brand Added Successfully")
            return redirect("brands")


class BrandDeleteView(DeleteView):
    model = Brand
    success_url = reverse_lazy('brands')
    success_message = "Brand Deleted Successfully"
    template_name = 'shop/brands.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ShopView(View):
    def get(self, request, pk=None):
        if pk:
            shop_obj = Shop.objects.get(id=pk)
            brand_choices_obj = Brand.objects.filter(user=request.user)
            return render(request, "shop/update_shop.html",
                          {"shop_obj": shop_obj, "brand_choices_obj": brand_choices_obj})
        else:
            user = request.user
            shop_obj = Shop.objects.filter(brand__user=user)
            brand_choices_obj = Brand.objects.filter(user=user)
            return render(request, "shop/shop.html", {"shop_obj": shop_obj, "brand_choices_obj": brand_choices_obj})

    def post(self, request, pk=None):
        if pk:
            shop_name = request.POST.get("shop_name")
            brand_id = request.POST.get("brand")
            shop_obj = Shop.objects.get(id=pk)
            shop_obj.name = shop_name
            shop_obj.brand_id = brand_id
            shop_obj.save()
            messages.success(request, "Shop updated successfully")
            return redirect('shop')
        else:
            shop_name = request.POST.get("shop_name")
            brand_id = request.POST.get("brand")
            Shop.objects.create(name=shop_name, brand_id=brand_id)
            messages.success(request, "Shop added successfully")
            return redirect('shop')


class ShopDetailView(View):
    def get(self, request, pk):
        shop_detail = Lager.objects.filter(shop_id=pk).first()
        current_balance = 0
        if shop_detail:
            current_balance = int(shop_detail.opening_balance) - int(shop_detail.credit) + int(shop_detail.debit) - int(
                shop_detail.credit)
        return render(request, "shop/shop_detail.html",
                      {"shop_detail": shop_detail, "current_balance": current_balance})


class ShopDeleteView(DeleteView):
    model = Shop
    success_url = reverse_lazy('shop')
    success_message = "Shop Deleted Successfully"
    template_name = 'shop/shop.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class LagerView(View):
    def get(self, request, pk=None):
        if pk:
            lager_obj = Lager.objects.filter(id=pk).first()
            shop_obj_choices = Shop.objects.filter(brand__user=request.user)
            return render(request, "shop/update_lager.html",
                          {"lager_obj": lager_obj, "shop_obj_choices": shop_obj_choices})
        else:
            user = request.user
            shop_obj_choices = Shop.objects.filter(brand__user=user)
            lager_obj = Lager.objects.filter(shop__brand__user=user)
            return render(request, "shop/lager.html", {"shop_obj_choices": shop_obj_choices, "lager_obj": lager_obj})

    def post(self, request, pk=None):
        if pk:
            shop_id = request.POST.get("shop")
            credit = request.POST.get("credit")
            debit = request.POST.get("debit")
            opening_balance = request.POST.get("opening_balance")
            lager_obj = Lager.objects.get(id=pk)
            lager_obj.shop_id = shop_id
            lager_obj.credit = credit
            lager_obj.debit = debit
            lager_obj.opening_balance = opening_balance
            lager_obj.save()
            messages.success(request, "Lager Updated Successfully")
            return redirect("lager")
        else:
            shop_id = request.POST.get("shop")
            credit = request.POST.get("credit")
            debit = request.POST.get("debit")
            opening_balance = request.POST.get("opening_balance")
            Lager.objects.create(shop_id=shop_id, credit=credit, debit=debit, opening_balance=opening_balance)
            messages.success(request, "Lager Added Successfully")
            return redirect("lager")


class LagerDeleteView(DeleteView):
    model = Lager
    success_url = reverse_lazy('lager')
    success_message = "Lager Deleted Successfully"
    template_name = 'shop/lager.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
