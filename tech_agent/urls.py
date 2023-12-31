"""
URL configuration for tech_agent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from accounts.views import MyTokenObtainPairView
from orders.views import CreateOrderView,UpdateOrderView

from rest_framework_simplejwt.views import (TokenRefreshView)
from django.contrib import admin
from django.urls import path,include
from orders.views import OrderAcceptanceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/customer/', include("customer.urls")),
    path('api/technician/', include("technician.urls")),
    path('api/orders/', include("orders.urls")),
    path('createorder/', CreateOrderView.as_view(), name='create-order'),
    path('updateorder/<int:order_id>/', UpdateOrderView.as_view(), name='update-order'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('acceptorder/<int:order_id>/', OrderAcceptanceView.as_view(), name='accept-order'),

]
