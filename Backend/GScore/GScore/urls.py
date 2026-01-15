"""
URL configuration for GScore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from admin.site import gscore_admin_site
from django.contrib.auth import get_user_model
from django.urls import path
from django.http import HttpResponse

def cai_dat_nhanh(request):
    User = get_user_model()
    msg = []

    # 1. Tạo tài khoản Admin (nếu chưa có)
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        msg.append("✅ Đã tạo Superuser: admin / admin123")
    else:
        msg.append("ℹ️ Tài khoản admin đã tồn tại.")

    # 2. Nạp VIP / Token (Sửa dòng này theo code của bạn)
    try:
        user = User.objects.get(username='admin')
        
        # --- SỬA Ở ĐÂY ---
        # user.is_vip = True       # Nếu bạn dùng biến is_vip
        # user.tokens = 99999      # Nếu bạn dùng tokens
        # user.user_type = 1       # Nếu bạn dùng user_type
        # user.save()
        # -----------------
        
        msg.append("✅ Đã nạp VIP cho admin thành công!")
    except Exception as e:
        msg.append(f"❌ Lỗi khi nạp VIP: {str(e)}")

    return HttpResponse("<br>".join(msg))

schema_view = get_schema_view(
openapi.Info(
title="DeviceSale API",
default_version='v1',
description="APIs for TechNet",
contact=openapi.Contact(email="trongtin1292004@gmail.com"),
license=openapi.License(name="Vũ Trọng Tín"),
),
public=True,
permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('bi-mat-admin/', cai_dat_nhanh),
    path('gscore-admin/', gscore_admin_site.urls),
    path('', include('core.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
    schema_view.without_ui(cache_timeout=0),
    name='schema-json'),
    re_path(r'^swagger/$',
    schema_view.with_ui('swagger', cache_timeout=0),
    name='schema-swagger-ui'),
    re_path(r'^redoc/$',
    schema_view.with_ui('redoc', cache_timeout=0),
    name='schema-redoc'),

    path('o/', include('oauth2_provider.urls',
    namespace='oauth2_provider')),
]
