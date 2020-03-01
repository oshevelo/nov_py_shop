from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),    
    path('admin/', admin.site.urls),

    path('authenticate/', include('apps.authenticate.urls')),
    path('products/', include('apps.products.urls')),
    path('shipments/', include('apps.shipments.urls')),
    path('users/', include('apps.users.urls')),
    path('carts/', include('apps.carts.urls')),
    path('orders/', include('apps.orders.urls')),
    path('catalogue/', include('apps.catalogue.urls')),
    path('payments/', include('apps.payments.urls')),
]