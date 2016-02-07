from django.shortcuts import render
from django.db.models import Max, Min

from django.http import Http404,  HttpResponseRedirect

import weblayout.models as wlm
import website.models as wsm
import webshop.models as wshm
import webform.forms as wfv

import random
from frankie_web_platform.settings import SIMILAR_PRODUCTS_NUM


from django.db.models import Q


class Parameter:
    def __init__(self, param_id, name, available_values=None, available_intervals=None, custom_values=None,
                 interval_checked=None, custom_value_checked=None, value_checked=None):
        self.param_id = param_id
        self.available_values = available_values
        self.available_intervals = available_intervals
        self.custom_values = custom_values
        self.name = name
        self.interval_checked = interval_checked
        self.custom_value_checked = custom_value_checked
        self.value_checked = value_checked


class Filter:
    def __init__(self, price_from_min, price_to_max, order_by):
        self.parameters = []
        self.price_from = price_from_min
        self.price_to = price_to_max
        self.order_by = order_by
        self.page = 0
        self.product_on_page = 100

    def append(self, parameter: Parameter) -> None:
        self.parameters.append(parameter)

    def __getitem__(self, item):
        return self.parameters[item]


class Product:
    def __init__(self, product=None, images=None, corrections=None):
        self.product = product
        self.images = images
        self.corrections = corrections


def get_all_values_from_request(request):
    get = dict(request.GET)
    if get.__len__() > 0:
        filter_items = []
        for elem in get:
            if elem == 'price_from':
                pass
            elif elem == 'price_to':
                pass
            elif elem == 'order_by':
                pass
            elif elem == 'page':
                pass
            elif elem == 'product_on_page':
                pass
            else:
                filter_items.append(elem.__str__().split('.'))
        # Filter
        params = []
        for param in filter_items:
            params.append(param[0])
        return params


def get_custom_values_from_request(request, param_id):
    get = dict(request.GET)
    if get.__len__() > 0:
        filter_items = []
        for elem in get:
            if elem == 'price_from':
                pass
            elif elem == 'price_to':
                pass
            elif elem == 'order_by':
                pass
            elif elem == 'page':
                pass
            elif elem == 'product_on_page':
                pass
            else:
                filter_items.append(elem.__str__().split('.'))
        # Filter
        custom_values = []
        for param in filter_items:
            if param[0] == param_id.__str__():
                if param[1] == '0':
                    custom_values.append(get[str.format("{0}.{1}", param[0], param[1])])
        return custom_values


def get_intervals_from_request(request, param_id):
    get = dict(request.GET)
    if get.__len__() > 0:
        filter_items = []
        for elem in get:
            if elem == 'price_from':
                pass
            elif elem == 'price_to':
                pass
            elif elem == 'order_by':
                pass
            elif elem == 'page':
                pass
            elif elem == 'product_on_page':
                pass
            else:
                filter_items.append(elem.__str__().split('.'))
        # Filter
        intervals = []
        for param in filter_items:
            if param[0] == param_id.__str__():
                if param[1] == '1':
                    intervals.append(get[str.format("{0}.{1}.{2}", param[0], param[1], param[2])][0])
        return intervals


def get_values_from_request(request, param_id):
    get = dict(request.GET)
    if get.__len__() > 0:
        filter_items = []
        for elem in get:
            if elem == 'price_from':
                pass
            elif elem == 'price_to':
                pass
            elif elem == 'order_by':
                pass
            elif elem == 'page':
                pass
            elif elem == 'product_on_page':
                pass
            else:
                filter_items.append(elem.__str__().split('.'))
        # Filter
        values = []
        for param in filter_items:
            if param[0] == param_id.__str__():
                if param[1] == '2':
                    values.append(get[str.format("{0}.{1}.{2}", param[0], param[1], param[2])])
        return values


def get_prices_from_request(request):
    get = dict(request.GET)
    price_from = 0
    price_to = 0
    if get.__len__() > 0:
        filter_items = []
        for elem in get:
            if elem == 'price_from':
                if get['price_from'][0].strip().__len__() > 0:
                    price_from = float((get['price_from'][0].replace(',', '.')))
            elif elem == 'price_to':
                if get['price_to'][0].strip().__len__() > 0:
                    price_to = float((get['price_to'][0].replace(',', '.')))
            elif elem == 'page':
                pass
            elif elem == 'product_on_page':
                pass
            elif elem == 'order_by':
                pass
            else:
                filter_items.append(elem.__str__().split('.'))
        # Filter
        return price_from, price_to


def get_order_by_from_request(request):
    get = dict(request.GET)
    if get.__len__() > 0:
        for elem in get:
            if elem == 'price_from':
                pass
            elif elem == 'price_to':
                pass
            elif elem == 'page':
                pass
            elif elem == 'product_on_page':
                pass
            elif elem == 'order_by':
                if get['order_by'][0].strip().__len__() > 0:
                    return get['order_by'][0]
    return None


def get_page_from_request(request):
    get = dict(request.GET)
    if get.__len__() > 0:
        for elem in get:
            if elem == 'price_from':
                pass
            elif elem == 'price_to':
                pass
            elif elem == 'page':
                if get['page'][0].strip().__len__() > 0:
                    return int(get['page'][0])
            elif elem == 'product_on_page':
                pass
            elif elem == 'order_by':
                pass
    return None


def get_product_on_page_from_request(request):
    get = dict(request.GET)
    if get.__len__() > 0:
        for elem in get:
            if elem == 'price_from':
                pass
            elif elem == 'price_to':
                pass
            elif elem == 'page':
                pass
            elif elem == 'product_on_page':
                if get['product_on_page'][0].strip().__len__() > 0:
                    return int(get['product_on_page'][0])
            elif elem == 'order_by':
                pass
    return None


def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def page(request, page_url):
    # try:
        # System Elements:
        sys_elem = wlm.SystemElement.objects.all()
        sys_header = sys_elem.filter(name='Header').first()
        sys_footer = sys_elem.filter(name='Footer').first()
        sys_script = sys_elem.filter(name='Script').first()

        # Banners:
        all_banners = wsm.Banner.objects.all()
        image_positions = wsm.Banners()
        if all_banners:
            for banner in all_banners:
                image_position = wsm.BannerImagePosition.objects.filter(banner=wsm.Banner.objects.filter(
                    name=banner.name).first()).all()
                image_positions.append(banner.name, image_position)

        order_by = get_order_by_from_request(request)
        prefilters = wshm.PreFilter.objects.all()
        pre_urls = []
        for prefilter in prefilters:
            pre_urls.append(prefilter.url)
        prefilter = None
        if page_url in pre_urls:
            prefilter = wshm.PreFilter.objects.filter(url=page_url).first()

            get_request = prefilter.gen_url()
            print(get_request)

        price_max = {'default_price__max': 0}
        price_min = {'default_price__min': 0}

        if not prefilter:
            # Category:
            category = wshm.Category.objects.filter(url=page_url).first()

            # SEO attributes:
            seo = {
                'title': category.title,
                'meta_description': category.meta_description,
                'meta_canonical': category.meta_canonical,
                'meta_robots': category.meta_robots,
                'h1': category.h1,
                'first_text': category.first_text,
                'second_text': category.second_text
            }

            # Prices:
            prices = get_prices_from_request(request)

            price_min = wshm.Product.objects.filter(category=category).aggregate(Min('default_price'))
            if price_min['default_price__min'] is None:
                price_min = {'default_price__min': 0}
            price_max = wshm.Product.objects.filter(category=category).aggregate(Max('default_price'))
            if price_max['default_price__max'] is None:
                price_max = {'default_price__max': 0}
            if prices is not None:
                price_min = {'default_price__min': prices[0]}
                price_max = {'default_price__max': prices[1]}

        else:
            seo = {
                'title': prefilter.title,
                'meta_description': prefilter.meta_description,
                'meta_canonical': prefilter.meta_canonical,
                'meta_robots': prefilter.meta_robots,
                'h1': prefilter.h1,
                'first_text': prefilter.first_text,
                'second_text': prefilter.second_text
            }
            category = prefilter.category
            if prefilter.price_from is not None:
                price_min = {'default_price__min': prefilter.price_from}
            if prefilter.price_to is not None:
                price_max = {'default_price__max': prefilter.price_to}

            request.GET = {}

            parameters = wshm.PreFilterParameterValue.objects.filter(pre_filter=prefilter).all()
            for parameter in parameters:
                if parameter.value_interval:
                    request.GET[str.format("{0}.1.{1}", parameter.product_parameter.id, parameter.value_interval.id)]\
                        = str(parameter.value_interval.id)
                else:
                    if parameter.value:
                        request.GET[str.format("{0}.2.{1}", parameter.product_parameter.id, parameter.value.id)] = \
                            str(parameter.value.id)
                    if parameter.custom_value:
                        request.GET[str.format("{0}.0", parameter.product_parameter.id)] = str(parameter.custom_value)

        if request.GET:
            if get_all_values_from_request(request):
                param_ids = remove_duplicates(get_all_values_from_request(request))
            else:
                param_ids = []
            if param_ids.__len__() > 0:
                params = wshm.ProductParameterValue.objects.filter(
                    category=category, product_parameter__in=param_ids).all()
                prod_params = wshm.ProductParameter.objects.filter(category=category, id__in=param_ids).all()
            else:
                params = wshm.ProductParameterValue.objects.filter(category=category).all()
                prod_params = wshm.ProductParameter.objects.filter(category=category).all()
            product_first_filter = {}

            for param in prod_params:
                if get_intervals_from_request(request, param.id):

                    intervals_get = get_intervals_from_request(request, param.id)
                    intervals = wshm.ProductParameterAvailableInterval.objects.filter(id__in=intervals_get[0])

                    for interval in intervals:
                        from_value = interval.from_value
                        to_value = interval.to_value
                        sort_as = param.sort_as

                        if from_value is not None and to_value is None:
                            products_params_ids = wshm.ProductParameterValue.objects.raw(
                                str.format('SELECT prod_vals.id \
                                FROM product_parameters_values as prod_vals \
                                LEFT JOIN product_parameters_available_value as val ON val.id=prod_vals.value_id \
                                JOIN product_parameters as prod_param ON prod_vals.product_parameter_id=prod_param.id \
                                WHERE CAST (val.value AS {1}) >= {0}) \
                                OR \
                                 CAST(prod_vals.custom_value AS {1}) >= {0})', from_value, sort_as))
                        elif from_value is None and to_value is not None:
                            products_params_ids = wshm.ProductParameterValue.objects.raw(
                                str.format('SELECT prod_vals.id \
                                FROM product_parameters_values as prod_vals \
                                LEFT JOIN product_parameters_available_value as val ON val.id=prod_vals.value_id \
                                JOIN product_parameters as prod_param ON prod_vals.product_parameter_id=prod_param.id \
                                WHERE CAST (val.value AS {1}) < {0}) \
                                OR \
                                 CAST(prod_vals.custom_value AS {1}) < {0})', to_value, sort_as))
                        else:
                            products_params_ids = wshm.ProductParameterValue.objects.raw(
                                str.format('SELECT prod_vals.id \
                                FROM product_parameters_values as prod_vals \
                                LEFT JOIN product_parameters_available_value as val ON val.id=prod_vals.value_id \
                                JOIN product_parameters as prod_param ON prod_vals.product_parameter_id=prod_param.id \
                                WHERE (CAST (val.value AS {2}) >= {0} \
                                AND CAST (val.value AS {2}) < {1}) \
                                OR \
                                (CAST(prod_vals.custom_value AS {2}) >= {0} \
                                AND CAST(prod_vals.custom_value AS {2}) < {1})', from_value, to_value, sort_as))

                        if products_params_ids:
                            params_ids = []
                            for product_param_id in products_params_ids:
                                params_ids.append(int(product_param_id.id))
                            product_first_filter[param.id] = wshm.ProductParameterValue.objects.filter(
                                id__in=params_ids).all()
                else:
                    custom_values = get_custom_values_from_request(request, param.id)
                    values = get_values_from_request(request, param.id)

                    for i in range(0, values.__len__()):
                        values[i] = values[i][0]

                    for i in range(0, custom_values.__len__()):
                        custom_values[i] = custom_values[i][0]

                    product_first_filter[param.id] = params.filter(product_parameter=param).all()
                    if custom_values.__len__() > 0 and values.__len__() > 0:
                        product_first_filter[param.id] = product_first_filter[param.id].filter(
                            Q(custom_value__in=custom_values) | Q(value__in=values)).all()
                    elif custom_values.__len__() > 0 and values.__len__() == 0:
                        product_first_filter[param.id] = product_first_filter[param.id].filter(
                            Q(custom_value__in=custom_values)).all()
                    elif custom_values.__len__() == 0 and values.__len__() > 0:
                        product_first_filter[param.id] = product_first_filter[param.id].filter(
                            value__in=values).all()

            products_ids = []
            i = 0
            res = []
            for product_param in product_first_filter:
                products_ids.append([])
                for product in product_first_filter[product_param]:
                    products_ids[i].append(product.product.id)
                i += 1
            if products_ids.__len__() > 1:
                for i in range(0, products_ids.__len__() - 1):
                    res = list(set(products_ids[i]) & set(products_ids[i + 1]))
            else:
                if products_ids.__len__() > 0:
                    res = products_ids[0]
                else:
                    res = []

            # Pagination
            page_number = get_page_from_request(request)
            product_on_page_num = get_product_on_page_from_request(request)
            if not page_number:
                page_number = 0
            if not product_on_page_num:
                product_on_page_num = 100

            if order_by == 'by date':
                products_filtered = wshm.Product.objects.filter(id__in=res,
                                                                default_price__gte=float(
                                                                    price_min['default_price__min']),
                                                                default_price__lte=float(
                                                                    price_max['default_price__max']),
                                                                category=category).order_by(
                    '-creation_date').all()[page_number * product_on_page_num: (page_number + 1) * product_on_page_num]
            elif order_by == 'by price asc':
                products_filtered = wshm.Product.objects.filter(id__in=res,
                                                                default_price__gte=float(
                                                                    price_min['default_price__min']),
                                                                default_price__lte=float(
                                                                    price_max['default_price__max']),
                                                                category=category).order_by(
                    'default_price').all()[page_number * product_on_page_num: (page_number + 1) * product_on_page_num]
            elif order_by == 'by price dsc':
                products_filtered = wshm.Product.objects.filter(id__in=res,
                                                                default_price__gte=float(
                                                                    price_min['default_price__min']),
                                                                default_price__lte=float(
                                                                    price_max['default_price__max']),
                                                                category=category).order_by(
                    '-default_price').all()[page_number * product_on_page_num: (page_number + 1) * product_on_page_num]
            else:
                products_filtered = wshm.Product.objects.filter(id__in=res,
                                                                default_price__gte=float(
                                                                    price_min['default_price__min']),
                                                                default_price__lte=float(
                                                                    price_max['default_price__max']),
                                                                category=category).order_by(
                    'weight').all()[page_number * product_on_page_num: (page_number + 1) * product_on_page_num]

        else:
            # Pagination
            page_number = get_page_from_request(request)
            product_on_page_num = get_product_on_page_from_request(request)
            if not page_number:
                page_number = 0
            if not product_on_page_num:
                product_on_page_num = 100

            if order_by == 'by date':
                products_filtered = wshm.Product.objects.filter(default_price__gte=float(
                    price_min['default_price__min']), default_price__lte=float(
                    price_max['default_price__max']), category=category).order_by(
                    '-creation_date').all()[page_number * product_on_page_num: (page_number + 1) * product_on_page_num]
            elif order_by == 'by price asc':
                products_filtered = wshm.Product.objects.filter(default_price__gte=float(
                    price_min['default_price__min']), default_price__lte=float(
                    price_max['default_price__max']), category=category).order_by(
                    'default_price').all()[page_number * product_on_page_num: (page_number + 1) * product_on_page_num]
            elif order_by == 'by price dsc':
                products_filtered = wshm.Product.objects.filter(default_price__gte=float(
                    price_min['default_price__min']),
                    default_price__lte=float(
                        price_max['default_price__max']), category=category).order_by(
                    '-default_price').all()[page_number * product_on_page_num: (page_number + 1) * product_on_page_num]
            else:
                products_filtered = wshm.Product.objects.filter(default_price__gte=float(
                    price_min['default_price__min']),
                    default_price__lte=float(
                        price_max['default_price__max']), category=category).order_by(
                    'weight').all()[page_number * product_on_page_num: (page_number + 1) * product_on_page_num]
            print(products_filtered)

        # Products:
        products = []
        product_image_position = wshm.ProductImagePosition.objects.filter(product__in=products_filtered).all()
        product_price_corrector = wshm.ProductPriceCorrector.objects.filter(product__in=products_filtered).all()
        for product in products_filtered:
            products.append(Product(
                product,
                product_image_position.filter(product=product).all(),
                product_price_corrector.filter(product=product).all()
            ))

        # Parameters:
        parameters = wshm.ProductParameter.objects.filter(category=category).order_by('weight').all()

        # Filter
        filter_parameters = Filter(price_min, price_max, order_by)

        if parameters:
            for param in parameters:

                interval = get_intervals_from_request(request, param.id)
                custom_val = get_custom_values_from_request(request, param.id)
                val = get_values_from_request(request, param.id)
                if interval:
                    for i in range(0, interval.__len__()):
                        interval[i] = int(interval[i])

                if custom_val:
                    custom_val = custom_val[0]

                if val:
                    for i in range(0, val.__len__()):
                        val[i] = int(val[i][0])

                available_values = wshm.ProductParameterAvailableValue.objects.filter(
                    product_parameter=param).all()
                available_intervals = wshm.ProductParameterAvailableInterval.objects.filter(
                    product_parameter=param).all()
                custom_value = wshm.ProductParameterValue.objects.filter(
                    product_parameter=param, category=category, value=None)  # .distinct('custom_value')
                if available_intervals.__len__() > 0:
                    filter_parameters.append(Parameter(param_id=param.id, name=param.name,
                                                       available_intervals=available_intervals,
                                                       interval_checked=interval))
                elif custom_value.__len__() > 0 and available_values.__len__() > 0:
                    filter_parameters.append(Parameter(param_id=param.id, name=param.name,
                                                       custom_values=custom_value,
                                                       available_values=available_values,
                                                       custom_value_checked=custom_val,
                                                       value_checked=val))
                elif custom_value.__len__() == 0 and available_values.__len__() > 0:
                    filter_parameters.append(Parameter(param_id=param.id, name=param.name,
                                                       available_values=available_values,
                                                       value_checked=val))
                elif custom_value.__len__() > 0 and available_values.__len__() == 0:
                    filter_parameters.append(Parameter(param_id=param.id, name=param.name,
                                                       custom_values=custom_value,
                                                       custom_value_checked=custom_val))
                elif param.name:
                    filter_parameters.append(Parameter(param_id=param.id, name=param.name))
                    print(param.name)
                filter_parameters.page = page_number
                filter_parameters.product_on_page = product_on_page_num

        form_feedback = wfv.FormFeedback()
        status, form_feedback = form_feedback.process(request=request)
        if status:
            return HttpResponseRedirect('/thanks')
        else:
            pass

        return render(request, category.template.path, {
            'seo': seo,
            'category': category,
            'additional_menu': wlm.AdditionalMenu.objects.all(),
            'extra_menu': wlm.ExtraMenu.objects.all(),
            'sys_header': sys_header,
            'sys_footer': sys_footer,
            'sys_script': sys_script,
            'banners': image_positions,
            'filter': filter_parameters,
            'form_feedback': form_feedback,
            'products': products,
            'max_page': int(products.__len__() / filter_parameters.product_on_page)
        })

    # except:
    #    raise Http404('Page not found')


def product_page(request, page_url):
    try:
        # System Elements:
        sys_elem = wlm.SystemElement.objects.all()
        sys_header = sys_elem.filter(name='Header').first()
        sys_footer = sys_elem.filter(name='Footer').first()
        sys_script = sys_elem.filter(name='Script').first()

        # Banners:
        all_banners = wsm.Banner.objects.all()
        image_positions = wsm.Banners()
        if all_banners:
            for banner in all_banners:
                image_position = wsm.BannerImagePosition.objects.filter(banner=wsm.Banner.objects.filter(
                    name=banner.name).first()).all()
                image_positions.append(banner.name, image_position)

        # Product:
        product = wshm.Product.objects.filter(url=page_url).first()
        product_images = wshm.ProductImagePosition.objects.filter(product=product).all()
        product_price_corrector = wshm.ProductPriceCorrector.objects.filter(product=product).all()

        # SEO attributes:
        seo = {
            'title': product.gen_title,
            'meta_description': product.gen_meta_description,
            'meta_canonical': product.meta_canonical,
            'meta_robots': product.meta_robots,
            'h1': product.gen_h1,
        }

        similar_products = wshm.Product.objects.filter(category=product.category).all()
        products_list = []
        for product_item in similar_products:
            products_list.append(Product(product_item, wshm.ProductImagePosition.objects.filter(product=product_item).
                                         all(),
                                         wshm.ProductPriceCorrector.objects.filter(product=product_item).all()))
        products = []
        ids = [product.id]
        i = 0
        j = 0
        while i < SIMILAR_PRODUCTS_NUM and j < 10:
            choice = random.choice(products_list)
            if choice.product.id not in ids:
                products.append(choice)
                ids.append(choice.product.id)
                i += 1
            j += 1
        if request.POST:
            result, form = wfv.FormRating.process(request)
        else:
            form = wfv.FormRating({'product_id': product.id})

        return render(request, product.template.path, {
            'seo': seo,
            'product': product,
            'product_images': product_images,
            'product_price_corrector': product_price_corrector,
            'main_menu': wlm.MainMenu.objects.all(),
            'additional_menu': wlm.AdditionalMenu.objects.all(),
            'extra_menu': wlm.ExtraMenu.objects.all(),
            'sys_header': sys_header,
            'sys_footer': sys_footer,
            'sys_script': sys_script,
            'banners': image_positions,
            'similar_products': products,
            'form_rating': form,
        })
    except:
        raise Http404('Page not found')

def generatestyle(request):

    pp_all = wshm.ProductParameter.objects.all()
    ppav_all = wshm.ProductParameterAvailableValue.objects.all()

    css_style = []

    pp = pp_all.filter(name='Цвет').all()
    for pp_item in pp:
        ppav = ppav_all.filter(product_parameter=pp_item).all()
        css_style.append(CssStyle(pp_item, ppav))


    return render(request, 'generatestyle.html', {
        'css_style': css_style,
        'test': pp
    })
