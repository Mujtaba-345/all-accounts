from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from users.views import LoginView
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', LoginView.as_view(), name='login'),
                  path('users/', include("users.urls"), name='users'),
                  path('shop/', include("shop.urls"), name='users')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# change the name of the admin site
admin.site.site_header = "All Accounts Administration"
admin.site.site_title = "All Accounts Admin Portal"
admin.site.index_title = "Welcome to All Accounts Admin Portal"
