from django.shortcuts import render
import json
from django.http import Http404, HttpResponseRedirect, HttpResponse

import weblayout.models as wlm
import website.models as wsm
import webshopcart.models as wshcm
import webshop.models as wshm


class Product:
    def __init__(self, product_id, count, price_corrector_id=None):
        self.product_id = product_id
        self.count = count
        self.price_corrector_id = price_corrector_id


def put_product(request):
    if request.POST:
        product_post = request.POST
        product_id = int(product_post['p'])
        if product_post['c'].strip().__len__() > 0:
            corrector_id = int(product_post['c'])
        else:
            corrector_id = None
        product_model = wshm.Product.objects.filter(id=product_id).first()
        if corrector_id:
            price_corrector = wshm.ProductPriceCorrector.objects.filter(product=product_model, id=corrector_id).first()
            if price_corrector:
                price = price_corrector.new_price
            else:
                price = product_model.default_price
        else:
            price = product_model.default_price

        image_url = wshm.ProductImagePosition.objects.filter(product=product_model).order_by('weight'). \
            first()
        if image_url:
            image_url = image_url.small_image()
        else:
            image_url = None

        if 'cart' not in request.session:
            request.session['cart'] = []

        flag = True
        count = 0

        for i in range(0, request.session['cart'].__len__()):
            if request.session['cart'][i]['p'] == product_id and request.session['cart'][i]['c'] == corrector_id:
                request.session['cart'][i]['count'] += 1
                flag = False
                count = request.session['cart'][i]['count']
                break
        if flag:
            request.session['cart'].append({'p': product_id, 'c': corrector_id, 'count': 1})
            count = 1

        t_count = 0
        t_price = 0
        for prod in request.session['cart']:
            t_count += prod['count']
            product_m = wshm.Product.objects.filter(id=prod['p']).first()
            price_c = wshm.ProductPriceCorrector.objects.filter(product=product_m, id=prod['c']).first()
            if price_c:
                p = price_c.new_price
            else:
                p = product_m.default_price
            t_price += p * prod['count']

        serialized = json.dumps({"img_url": image_url, "p_url": product_model.url, "p_name": product_model.name,
                                 "p_count": count, "t_count": t_count, "t_price": t_price, "price": price})
        return HttpResponse(serialized, content_type="application/json")
    return HttpResponse("{}", content_type="application/json")


def dec_product(request):
    if request.POST:
        product_post = request.POST
        product_id = int(product_post['p'])
        if product_post['c'].strip().__len__() > 0:
            corrector_id = int(product_post['c'])
        else:
            corrector_id = None

        product_model = wshm.Product.objects.filter(id=product_id).first()

        if corrector_id:
            price_corrector = wshm.ProductPriceCorrector.objects.filter(product=product_model, id=corrector_id).first()
            if price_corrector:
                price = price_corrector.new_price
            else:
                price = product_model.default_price
        else:
            price = product_model.default_price

        image_url = wshm.ProductImagePosition.objects.filter(product=product_model).order_by('weight'). \
            first()
        if image_url:
            image_url = image_url.small_image()
        else:
            image_url = None

        count = 0
        if 'cart' in request.session:
            for i in range(0, request.session['cart'].__len__()):
                if request.session['cart'][i]['p'] == product_id and request.session['cart'][i]['c'] == corrector_id:
                    if request.session['cart'][i]['count'] > 1:
                        request.session['cart'][i]['count'] -= 1
                        count = request.session['cart'][i]['count']
                    break
        t_count = 0
        t_price = 0
        for prod in request.session['cart']:
            t_count += prod['count']
            product_m = wshm.Product.objects.filter(id=prod['p']).first()
            price_c = wshm.ProductPriceCorrector.objects.filter(product=product_m, id=prod['c']).first()
            if price_c:
                p = price_c.new_price
            else:
                p = product_m.default_price
            t_price += p * prod['count']

        serialized = json.dumps({"img_url": image_url, "p_url": product_model.url, "p_name": product_model.name,
                                 "p_count": count, "t_count": t_count, "t_price": t_price, "price": price})
        return HttpResponse(serialized, content_type="application/json")
    return HttpResponse("{}", content_type="application/json")


def del_product(request):
    if request.POST:
        product_post = request.POST
        product_id = int(product_post['p'])
        if product_post['c'].strip().__len__() > 0:
            corrector_id = int(product_post['c'])
        else:
            corrector_id = None

        product_model = wshm.Product.objects.filter(id=product_id).first()

        if corrector_id:
            price_corrector = wshm.ProductPriceCorrector.objects.filter(product=product_model, id=corrector_id).first()
            if price_corrector:
                price = price_corrector.new_price
            else:
                price = product_model.default_price
        else:
            price = product_model.default_price

        image_url = wshm.ProductImagePosition.objects.filter(product=product_model).order_by('weight'). \
            first()
        if image_url:
            image_url = image_url.small_image()
        else:
            image_url = None

        count = 0
        if 'cart' in request.session:
            for i in range(0, request.session['cart'].__len__()):
                if request.session['cart'][i]['p'] == product_id and request.session['cart'][i]['c'] == corrector_id:
                    request.session['cart'].__delitem__(i)
                    break

        t_count = 0
        t_price = 0
        for prod in request.session['cart']:
            t_count += prod['count']
            product_m = wshm.Product.objects.filter(id=prod['p']).first()
            price_c = wshm.ProductPriceCorrector.objects.filter(product=product_m, id=prod['c']).first()
            if price_c:
                p = price_c.new_price
            else:
                p = product_m.default_price
            t_price += p * prod['count']

        serialized = json.dumps({"img_url": image_url, "p_url": product_model.url, "p_name": product_model.name,
                                 "p_count": count, "t_count": t_count, "t_price": t_price, "price": price})
        return HttpResponse(serialized, content_type="application/json")
    return HttpResponse("{}", content_type="application/json")


def get_products(request):
    if request.POST:
        products = {}
        t_price = 0
        t_count = 0
        if 'cart' in request.session:
            for prod in request.session['cart']:
                product = wshm.Product.objects.filter(id=prod['p']).first()
                img_url = wshm.ProductImagePosition.objects.filter(product=product).order_by('weight').first()
                if img_url:
                    img_url = img_url.small_image()
                price_corrector = wshm.ProductPriceCorrector.objects.filter(id=prod['c']).first()
                if price_corrector:
                    price = price_corrector.new_price
                else:
                    price = product.default_price
                t_count += prod['count']
                t_price += prod['count'] * price
                if price_corrector:
                    products[product.id.__str__() + '_' + price_corrector.id.__str__()] = {'p': product.id,
                                                                                           'c': price_corrector.id,
                                                                                           'img_url': img_url,
                                                                                           'p_name': product.name,
                                                                                           'p_count': prod['count'],
                                                                                           'price': price}
                else:
                    products[product.id.__str__()] = {'p': product.id, 'c': None,
                                                      'img_url': img_url, 'p_name': product.name,
                                                      'p_count': prod['count'], 'price': price}

                products['t_price'] = t_price
                products['t_count'] = t_count

        serialized = json.dumps(products)
        return HttpResponse(serialized, content_type="application/json")
    return HttpResponse("{}", content_type="application/json")


def clear_cart(request):
    if request.POST:
        if 'cart' in request.session:
            request.session.__delitem__('cart')
    return HttpResponse("{}", content_type="application/json")


def cart_page(request):
    try:
        if request.POST:
            products = []
            products_post = request.POST.getlist('product_positions')
            for product in products_post:
                product_tmp = product.split(';')
                if product_tmp.__len__() == 3:
                    products.append(Product(product_tmp[0], product_tmp[1], product_tmp[2]))
                elif product_tmp.__len__() == 2:
                    products.append(Product(product_tmp[0], product_tmp[1]))
                else:
                    pass
            cart_order = wshcm.ProductCart()
            cart_order.username = request.POST['user_name']
            cart_order.email = request.POST['user_email']
            cart_order.fixed_sum = request.POST['total_price']
            cart_order.phone = request.POST['user_phone']
            cart_order.save()
            for product in products:
                product_tmp = wshcm.ProductInCart()
                product_tmp.product_id = product.product_id
                product_tmp.cart = cart_order
                product_tmp.count = product.count
                if product.price_corrector_id:
                    product_tmp.price_correction = wshm.ProductPriceCorrector.objects.filter(
                        id=product.price_corrector_id).first()
                product_tmp.save()
            return HttpResponseRedirect('/thanks')
                
        # Banners:
        all_banners = wsm.Banner.objects.all()
        image_positions = wsm.Banners()
        if all_banners:
            for banner in all_banners:
                image_position = wsm.BannerImagePosition.objects.filter(banner=wsm.Banner.objects.filter(
                    name=banner.name).first()).all()
                image_positions.append(banner.name, image_position)

        return render(request, 'cart.html', {
            'main_menu': wlm.MainMenu.objects.all(),
            'additional_menu': wlm.AdditionalMenu.objects.all(),
            'extra_menu': wlm.ExtraMenu.objects.all(),
            'banners': image_positions,
        })
    except:
        raise Http404('Page not found')
