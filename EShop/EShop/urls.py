from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

    path('admin/', admin.site.urls),
    path('auth/', include('apps.authenticate.urls')),
    path('products/', include('apps.products.urls')),
    path('carts/', include('apps.carts.urls')),
    path('orders/', include('apps.orders.urls')),
    path('payments/', include('apps.payments.urls')),
]
