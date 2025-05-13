from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from users.views import logout_view,login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('logout/', logout_view, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
