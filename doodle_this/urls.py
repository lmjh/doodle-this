from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
    path('account/', include('accounts.urls')),
    path('prints/', include('prints.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('prompts/', include('prompts.urls')),
    path('faq/', TemplateView.as_view(template_name="faq.html"), name='faq'),
    path('', include('sketchbook.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
