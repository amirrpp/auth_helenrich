from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

# Website App Views
import website.views

# Web shop App Views
import webshop.views

# Web shop cart App Views
import webshopcart.views

# Web rating App Views
import webrating.views

from webaccount.views import AccountAuthView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalogue/generatestyle', webshop.views.generatestyle),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^catalogue/(\w+)', webshop.views.page, name='shop_page'),
    url(r'^product/(\w+)', webshop.views.product_page, name='product_page'),
    url(r'^cart', webshopcart.views.cart_page),
    url(r'^comments', webrating.views.comments),
    url(r'^auth$', AccountAuthView.as_view(), name='login_registration'),
    url(r'^(\w+)$', website.views.page, name='page'),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', website.views.index_page),
    url(r'^api/add_product$', webshopcart.views.put_product),
    url(r'^api/dec_product$', webshopcart.views.dec_product),
    url(r'^api/clear_cart$', webshopcart.views.clear_cart),
    url(r'^api/del_product$', webshopcart.views.del_product),
    url(r'^api/get_products$', webshopcart.views.get_products),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
