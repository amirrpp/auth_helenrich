from django.db import models
from django.db.models import Avg
import re

# WebLayout models
from weblayout.models import Template

# Ckeditor support
from ckeditor.fields import RichTextField

# Chained selects support
from smart_selects.db_fields import ChainedForeignKey

# Image cropping support and thumbnails engine
from image_cropping import ImageRatioField
from easy_thumbnails.files import get_thumbnailer

# Config variables
from frankie_web_platform.settings import PRODUCT_IMAGE_LARGE, PRODUCT_IMAGE_MEDIUM, PRODUCT_IMAGE_SMALL


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    url = models.CharField(max_length=256, unique=True)
    title = models.CharField(max_length=256)
    first_text = RichTextField(null=True, blank=True)
    second_text = RichTextField(null=True, blank=True)
    meta_description = models.CharField(max_length=256,
                                        null=True, blank=True)
    meta_canonical = models.CharField(max_length=256,
                                      null=True, blank=True)
    meta_robots = models.CharField(max_length=256,
                                   null=True, blank=True)
    h1 = models.CharField(max_length=256,
                          null=True, blank=True)
    description = models.CharField(max_length=256,
                                   null=True, blank=True)
    first_image = models.ImageField(
        upload_to="products/", null=True, blank=True)
    second_image = models.ImageField(
        upload_to="products/", null=True, blank=True)
    template = models.ForeignKey(Template)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)
    title_generation_rule = models.CharField(max_length=256, null=True, blank=True)
    meta_description_generation_rule = models.CharField(max_length=256, null=True, blank=True)
    h1_generation_rule = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductImagePosition(models.Model):
    id = models.AutoField(primary_key=True)
    image_original = models.ImageField(
        upload_to="image_positions/products/")
    cropping_large = ImageRatioField('image_original', PRODUCT_IMAGE_LARGE)
    cropping_medium = ImageRatioField('image_original', PRODUCT_IMAGE_MEDIUM)
    cropping_small = ImageRatioField('image_original', PRODUCT_IMAGE_SMALL)

    name = models.CharField(max_length=256, unique=True)
    title = models.CharField(max_length=256)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)
    weight = models.IntegerField()
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    product = models.ForeignKey('Product')

    def __str__(self):
        return self.name

    def original_image(self):
        return str.format("<img src=/media/{0} alt='Original Image: {1}' width=200/>", self.image_original, self.title)

    original_image.short_description = 'Original'
    original_image.allow_tags = True

    def large_image(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (PRODUCT_IMAGE_LARGE[:PRODUCT_IMAGE_LARGE.index('x')],
                     PRODUCT_IMAGE_LARGE[PRODUCT_IMAGE_LARGE.index('x') + 1:]),
            'box': self.cropping_large,
            'crop': True,
            'detail': True,
        }).url
        return url

    large_image.allow_tags = True

    def small_image(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (PRODUCT_IMAGE_SMALL[:PRODUCT_IMAGE_SMALL.index('x')],
                     PRODUCT_IMAGE_SMALL[PRODUCT_IMAGE_SMALL.index('x') + 1:]),
            'box': self.cropping_small,
            'crop': True,
            'detail': True,
        }).url
        return url

    small_image.allow_tags = True

    def medium_image(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (PRODUCT_IMAGE_MEDIUM[:PRODUCT_IMAGE_MEDIUM.index('x')],
                     PRODUCT_IMAGE_MEDIUM[PRODUCT_IMAGE_MEDIUM.index('x') + 1:]),
            'box': self.cropping_medium,
            'crop': True,
            'detail': True,
        }).url
        return url

    medium_image.allow_tags = True

    def large_image_admin(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (PRODUCT_IMAGE_LARGE[:PRODUCT_IMAGE_LARGE.index('x')],
                     PRODUCT_IMAGE_LARGE[PRODUCT_IMAGE_LARGE.index('x') + 1:]),
            'box': self.cropping_large,
            'crop': True,
            'detail': True,
        }).url
        return str.format('<img src={0} width=200 />', url)

    large_image_admin.allow_tags = True

    def small_image_admin(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (PRODUCT_IMAGE_SMALL[:PRODUCT_IMAGE_SMALL.index('x')],
                     PRODUCT_IMAGE_SMALL[PRODUCT_IMAGE_SMALL.index('x') + 1:]),
            'box': self.cropping_small,
            'crop': True,
            'detail': True,
        }).url
        return str.format('<img src={0} width=200 />', url)

    small_image_admin.allow_tags = True

    def medium_image_admin(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (PRODUCT_IMAGE_MEDIUM[:PRODUCT_IMAGE_MEDIUM.index('x')],
                     PRODUCT_IMAGE_MEDIUM[PRODUCT_IMAGE_MEDIUM.index('x') + 1:]),
            'box': self.cropping_medium,
            'crop': True,
            'detail': True,
        }).url
        return str.format('<img src={0} width=200 />', url)

    medium_image_admin.allow_tags = True

    class Meta:
        db_table = 'product_image_positions'
        verbose_name = 'Product Image Position'
        verbose_name_plural = 'Product Image Positions'


class ProductPriceCorrector(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    name = models.CharField(max_length=256, unique=True)
    new_price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_price_correctors'
        verbose_name = 'Product Price Correction'
        verbose_name_plural = 'Product Price Corrections'


class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    percent = models.FloatField()
    image = models.ImageField(null=True, blank=True, upload_to="sales/")

    class Meta:
        db_table = 'sales'
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'


class Margin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    percent = models.FloatField()

    class Meta:
        db_table = 'margins'
        verbose_name = 'Margin'
        verbose_name_plural = 'Margins'


class DeliveryRule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    from_mass = models.FloatField(null=True, blank=True)
    to_mass = models.FloatField(null=True, blank=True)
    price = models.FloatField()

    class Meta:
        db_table = 'delivery_rules'
        verbose_name = 'Delivery Rule'
        verbose_name_plural = 'Delivery Rules'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=256, unique=True)
    url = models.CharField(max_length=256, unique=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    default_price = models.FloatField()
    active = models.BooleanField(default=True)
    first_text = RichTextField(null=True, blank=True)
    second_text = RichTextField(null=True, blank=True)
    meta_description = models.CharField(max_length=256,
                                        null=True, blank=True)
    meta_canonical = models.CharField(max_length=256,
                                      null=True, blank=True)
    meta_robots = models.CharField(max_length=256,
                                   null=True, blank=True)
    h1 = models.CharField(max_length=256,
                          null=True, blank=True)
    description = models.CharField(max_length=256,
                                   null=True, blank=True)

    template = models.ForeignKey(Template)
    special_proposition = models.ForeignKey('SpecialProposition', null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)
    provider = models.ForeignKey('Provider')
    category = models.ForeignKey(Category)
    weight = models.IntegerField(default=0)
    mass = models.FloatField(default=0)
    sale = models.ForeignKey(Sale, null=True, blank=True)
    margin = models.ForeignKey(Margin, null=True, blank=True)

    def __str__(self):
        return self.name

    def gen_title(self):
        title_generation_rule = self.category.title_generation_rule
        res = []
        if (self.title is None or self.title.strip().__len__() == 0) and title_generation_rule is not None:
            params_names = re.findall(r'\[(\w+)\]', title_generation_rule)
            params = ProductParameter.objects.filter(name__in=params_names)
            parameter_values = ProductParameterValue.objects.filter(product=self, product_parameter__in=params)
            for param in params_names:
                parameter_result = parameter_values.filter(product_parameter=params.filter(name=param)).first()
                if param == 'name':
                    res.append(self.name)
                if param == 'special_proposition':
                    if self.special_proposition:
                        res.append(self.special_proposition.name)
                    else:
                        res.append('')
                else:
                    if parameter_result:
                        if parameter_result.value:
                            res.append(parameter_result.value.value)
                        elif parameter_result.custom_value:
                            res.append(parameter_result.custom_value)

            for item in res:
                title_generation_rule = re.sub(r'\[(\w+)\]', item, title_generation_rule, 1)

            if not self.title:
                return self.title
            if (title_generation_rule is None) or title_generation_rule.strip().__len__() == 0:
                return self.title
            if res.__len__() < params_names.__len__():
                return self.title
        else:
            return self.title
        return title_generation_rule

    def gen_h1(self):
        h1_generation_rule = self.category.h1_generation_rule
        res = []
        if (self.h1 is None or self.h1.strip().__len__() == 0) and h1_generation_rule is not None:
            params_names = re.findall(r'\[(\w+)\]', h1_generation_rule)
            params = ProductParameter.objects.filter(name__in=params_names)
            parameter_values = ProductParameterValue.objects.filter(product=self, product_parameter__in=params)
            for param in params_names:
                parameter_result = parameter_values.filter(product_parameter=params.filter(name=param)).first()
                if param == 'name':
                    res.append(self.name)
                elif param == 'special_proposition':
                    if self.special_proposition:
                        res.append(self.special_proposition.name)
                    else:
                        res.append('')
                else:
                    if parameter_result:
                        if parameter_result.value:
                            res.append(parameter_result.value.value)
                        elif parameter_result.custom_value:
                            res.append(parameter_result.custom_value)

            for item in res:
                h1_generation_rule = re.sub(r'\[(\w+)\]', item, h1_generation_rule, 1)

            if not self.h1:
                return self.h1
            if (h1_generation_rule is None) or h1_generation_rule.strip().__len__() == 0:
                return self.h1
            if res.__len__() < params_names.__len__():
                return self.h1
        else:
            return self.h1
        return h1_generation_rule

    def gen_meta_description(self):
        meta_description_generation_rule = self.category.meta_description_generation_rule
        res = []
        if (self.meta_description is None or self.meta_description.strip().__len__() == 0) \
                and meta_description_generation_rule is not None:
            params_names = re.findall(r'\[(\w+)\]', meta_description_generation_rule)
            params = ProductParameter.objects.filter(name__in=params_names)
            parameter_values = ProductParameterValue.objects.filter(product=self, product_parameter__in=params)
            for param in params_names:
                parameter_result = parameter_values.filter(product_parameter=params.filter(name=param)).first()
                if param == 'name':
                    res.append(self.name)
                elif param == 'special_proposition':
                    if self.special_proposition:
                        res.append(self.special_proposition.name)
                    else:
                        res.append('')
                else:
                    if parameter_result:
                        if parameter_result.value:
                            res.append(parameter_result.value.value)
                        elif parameter_result.custom_value:
                            res.append(parameter_result.custom_value)

            for item in res:
                meta_description_generation_rule = re.sub(r'\[(\w+)\]', item, meta_description_generation_rule, 1)

            if not self.meta_description:
                return self.meta_description
            if (meta_description_generation_rule is None) or meta_description_generation_rule.strip().__len__() == 0:
                return self.meta_description
            if res.__len__() < params_names.__len__():
                return self.meta_description

        return meta_description_generation_rule

    def get_delivery_price(self):
        delivery_rules = DeliveryRule.objects.all()
        if delivery_rules:
            for rule in delivery_rules:
                if rule.from_mass is not None and rule.to_mass is not None:
                    if rule.from_mass <= self.mass < rule.to_mass:
                        return rule.price
                elif rule.from_mass is None and rule.to_mass is not None:
                    if self.mass < rule.to_mass:
                        return rule.price
                elif rule.from_mass is not None and rule.to_mass is None:
                    if self.mass >= rule.from_mass:
                        return rule.price
        return 0

    def get_avg_rating(self):
        ratings = ProductRating.objects.filter(product=self, state=True).all()
        avg = 0
        if ratings.__len__() > 0:
            avg = ratings.aggregate(Avg('rating'))
            return avg['rating__avg']
        return avg

    def get_new_comments(self):
        return ProductRating.objects.filter(product=self, state=False).all().__len__()

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        unique_together = ('name', 'category')


class ProductRating(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product)
    user_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    comment = RichTextField()
    rating = models.FloatField()
    state = models.BooleanField(default=False)
    date_on_add = models.DateField(auto_now=True, blank=True)

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'product_ratings'
        verbose_name = 'Ratings and comments for product'
        verbose_name_plural = 'Rating and comment for product'


class SpecialProposition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    image = models.ImageField('special_propositions/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'special_propositions'
        verbose_name = 'Special Proposition'
        verbose_name_plural = 'Special Propositions'


class ProductParameter(models.Model):
    SORT_AS = (
        ('BOOLEAN', 'BOOLEAN'),
        ('INTEGER', 'INTEGER'),
        ('STRING', 'STRING'),
        ('FLOAT', 'FLOAT'))
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    sort_as = models.CharField(max_length=32, choices=SORT_AS)
    first_image = models.ImageField(upload_to="product_parameter/", null=True, blank=True)
    second_image = models.ImageField(upload_to="product_parameter/", null=True, blank=True)
    category = models.ForeignKey(Category)
    prefix = models.CharField(max_length=8, null=True, blank=True)
    suffix = models.CharField(max_length=8, null=True, blank=True)
    weight = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_parameters'
        verbose_name = 'Product Parameter'
        verbose_name_plural = 'Product Parameters'
        unique_together = ('name', 'category')


class ProductParameterAvailableValue(models.Model):
    id = models.AutoField(primary_key=True)
    product_parameter = models.ForeignKey('ProductParameter')
    value = models.CharField(max_length=256)
    first_image = models.ImageField(upload_to="product_parameter_value/", null=True, blank=True)
    second_image = models.ImageField(upload_to="product_parameter_value/", null=True, blank=True)
    weight = models.IntegerField()

    def __str__(self):
        return self.value

    class Meta:
        unique_together = ('product_parameter', 'value')
        db_table = 'product_parameters_available_value'
        verbose_name = 'Product Parameter Available Value'
        verbose_name_plural = 'Product Parameter Available Values'


class ProductParameterAvailableInterval(models.Model):
    id = models.AutoField(primary_key=True)
    product_parameter = models.ForeignKey('ProductParameter')
    name = models.CharField(max_length=256)
    from_value = models.FloatField(null=True, blank=True)
    to_value = models.FloatField(null=True, blank=True)
    first_image = models.ImageField(upload_to="product_parameter_interval/", null=True, blank=True)
    second_image = models.ImageField(upload_to="product_parameter_interval/", null=True, blank=True)
    weight = models.IntegerField()

    def __str__(self):
        return str.format("From {0} {1} {2} to {0} {1} {2}", self.product_parameter.prefix,
                          self.from_value, self.product_parameter.suffix, self.to_value)

    class Meta:
        unique_together = ('name', 'product_parameter')
        db_table = 'product_parameters_available_intervals'
        verbose_name = 'Product Parameter Available Interval'
        verbose_name_plural = 'Product Parameter Available Intervals'


class ProductParameterValue(models.Model):
    product = models.ForeignKey(Product)
    category = models.ForeignKey(Category)
    product_parameter = ChainedForeignKey(
        ProductParameter,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
    )
    value = ChainedForeignKey(
        ProductParameterAvailableValue,
        chained_field="product_parameter",
        chained_model_field="product_parameter",
        show_all=False,
        auto_choose=True,
        null=True,
        blank=True
    )
    custom_value = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return str.format("Product: {0} => {1} => {2} | {3}",
                          self.product, self.product_parameter, self.value, self.custom_value)

    class Meta:
        unique_together = ('product', 'category', 'product_parameter')
        db_table = 'product_parameters_values'
        verbose_name = 'Product Parameter Value'
        verbose_name_plural = 'Product Parameter Values'


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    short_name = models.CharField(max_length=3)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'currencies'
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    currency = models.ForeignKey(Currency)
    coefficient = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'providers'
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'


class PreFilter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    category = models.ForeignKey(Category)
    price_from = models.FloatField(null=True, blank=True)
    price_to = models.FloatField(null=True, blank=True)
    url = models.CharField(max_length=256, unique=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    active = models.BooleanField(default=True)
    first_text = RichTextField(null=True, blank=True)
    second_text = RichTextField(null=True, blank=True)
    meta_description = models.CharField(max_length=256,
                                        null=True, blank=True)
    meta_canonical = models.CharField(max_length=256,
                                      null=True, blank=True)
    meta_robots = models.CharField(max_length=256,
                                   null=True, blank=True)
    h1 = models.CharField(max_length=256,
                          null=True, blank=True)
    description = models.CharField(max_length=256,
                                   null=True, blank=True)
    ORDER = (('by weight', 'by weight'),
             ('by price asc', 'by price asc'),
             ('by price dsc', 'by price dsc'),
             ('by date', 'by date')
             )

    order = models.CharField(max_length=256, choices=ORDER)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'pre_filters'
        verbose_name = 'PreFilter'
        verbose_name_plural = 'PreFilters'

    def gen_url(self):
        url = str.format("/{0}/{1}?price_from={2}&price_to={3}&order_by={4}", 'catalogue',
                         self.category.url, self.price_from, self.price_to, self.order)
        parameters = PreFilterParameterValue.objects.filter(pre_filter=self).all()
        for parameter in parameters:
            if parameter.value_interval:
                url += str.format("&{0}.1.{1}={1}", parameter.product_parameter.id, parameter.value_interval.id)
            else:
                if parameter.value:
                    url += str.format("&{0}.2.{1}={1}", parameter.product_parameter.id, parameter.value.id)
                if parameter.custom_value:
                    url += str.format("&{0}.0={1}", parameter.product_parameter.id, parameter.custom_value)
        return url


class PreFilterParameterValue(models.Model):
    pre_filter = models.ForeignKey(PreFilter)
    category = models.ForeignKey(Category)
    product_parameter = ChainedForeignKey(
        ProductParameter,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True
    )
    value = ChainedForeignKey(
        ProductParameterAvailableValue,
        chained_field="product_parameter",
        chained_model_field="product_parameter",
        show_all=False,
        auto_choose=True,
        null=True,
        blank=True
    )
    custom_value = models.CharField(max_length=256, null=True, blank=True)
    value_interval = ChainedForeignKey(
        ProductParameterAvailableInterval,
        chained_field="product_parameter",
        chained_model_field="product_parameter",
        show_all=False,
        auto_choose=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return str.format("PreFilter: {0} => {1} => {2} | {3}",
                          self.pre_filter, self.product_parameter, self.value, self.custom_value)

    class Meta:
        unique_together = (("pre_filter", "product_parameter"),)
        db_table = 'pre_filter_parameters_value'
        verbose_name = 'PreFilter Parameter Value'
        verbose_name_plural = 'PreFilter Parameter Values'
