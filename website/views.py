from django.shortcuts import render

from django.http import Http404

import weblayout.models as wlm
import website.models as wsm
import webshop.models as wshm


class Product:
    def __init__(self, product=None, images=None, corrections=None):
        self.product = product
        self.images = images
        self.corrections = corrections

def page(request, page_url):
    try:
        # System Elements:
        sys_elem = wlm.SystemElement.objects.all()
        sys_header = sys_elem.filter(name='Header').first()
        sys_footer = sys_elem.filter(name='Footer').first()
        sys_script = sys_elem.filter(name='Script').first()

        # Static Page:
        static_page = wsm.StaticPage.objects.filter(url=page_url).first()

        # SEO attributes:
        seo = {
            'title': static_page.title,
            'meta_description': static_page.meta_description,
            'meta_canonical': static_page.meta_canonical,
            'meta_robots': static_page.meta_robots,
            'h1': static_page.h1,
        }

        # Galleries:
        gallery = None
        if static_page.gallery:
            gallery = wsm.GalleryImagePosition.objects.filter(gallery=wsm.Gallery.objects.filter(
                name=static_page.gallery.name).first()).all()

        # Banners:
        all_banners = wsm.Banner.objects.all()
        image_positions = wsm.Banners()
        if all_banners:
            for banner in all_banners:
                image_position = wsm.BannerImagePosition.objects.filter(banner=wsm.Banner.objects.filter(
                    name=banner.name).first()).all()
                image_positions.append(banner.name, image_position)

        # Top Sales:
        products = wshm.Product.objects.filter(special_proposition=wshm.SpecialProposition.objects.filter(name='top-sales').first()).all()
        top_products = []
        product_image_position = wshm.ProductImagePosition.objects.filter(product__in=products).all()
        product_price_corrector = wshm.ProductPriceCorrector.objects.filter(product__in=products).all()
        for product in products:
            top_products.append(Product(
                product,
                product_image_position.filter(product=product).all(),
                product_price_corrector.filter(product=product).all()
            ))      

        return render(request, static_page.template.path, {
            'seo': seo,
            'static_page': static_page,
            'additional_menu': wlm.AdditionalMenu.objects.all(),
            'extra_menu': wlm.ExtraMenu.objects.all(),
            'sys_header': sys_header,
            'sys_footer': sys_footer,
            'sys_script': sys_script,
            'banners': image_positions,
            'gallery': gallery,
            'top_products':top_products,
        })
    except:
        raise Http404('Page not found')


def index_page(request):
    return page(request, 'index')
