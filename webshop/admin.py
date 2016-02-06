from django.contrib import admin
from webshop.models import *
from image_cropping import ImageCroppingMixin


class ProductParametersInline(admin.TabularInline):
    model = ProductParameterValue


class ProductParameterAvailableValueInline(admin.TabularInline):
    model = ProductParameterAvailableValue
    show_change_link = True


class ProductRatingsInline(admin.StackedInline):
    model = ProductRating
    show_change_link = True
    extra = 0


class ProductParameterAvailableIntervalInline(admin.TabularInline):
    model = ProductParameterAvailableInterval
    show_change_link = True


class ProductParametersCategoryInline(admin.TabularInline):
    model = ProductParameter
    show_change_link = True


class ProductParameterAdmin(admin.ModelAdmin):
    inlines = (ProductParameterAvailableValueInline, ProductParameterAvailableIntervalInline)


class CategoryAdmin(admin.ModelAdmin):
    inlines = (ProductParametersCategoryInline, )


class PreFilterParametersInline(admin.TabularInline):
    model = PreFilterParameterValue


class ProductImagePositionAdminInline(admin.TabularInline):
    model = ProductImagePosition
    exclude = ('cropping_large', 'cropping_small', 'cropping_medium', )
    extra = 0
    show_change_link = True


class ProductPriceCorrectorInline(admin.TabularInline):
    model = ProductPriceCorrector
    extra = 0


class HasNewCommentsListFilter(admin.SimpleListFilter):
    title = 'Has new comments'

    parameter_name = 'comments_num'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('with_new', 'With new comments'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'with_new':
            products_ratings = ProductRating.objects.filter(state=False).all()
            products = []
            for rating in products_ratings:
                products.append(rating.product.id)
            return queryset.filter(id__in=products).all()


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'gen_title', 'gen_meta_description', 'gen_h1', 'get_delivery_price', 'get_avg_rating',
                    'get_new_comments')
    inlines = (ProductParametersInline, ProductImagePositionAdminInline, ProductPriceCorrectorInline,
               ProductRatingsInline)
    list_filter = ('category', HasNewCommentsListFilter)


class PreFilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'gen_url')
    inlines = (PreFilterParametersInline, )


class ProductImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'last_edit_date', 'weight', 'active', 'title', 'description',
                    'original_image', 'large_image_admin', 'medium_image_admin', 'small_image_admin')
    list_filter = ('product',)


admin.site.register(ProductImagePosition, ProductImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductParameter, ProductParameterAdmin)
admin.site.register(ProductParameterValue)
admin.site.register(ProductParameterAvailableValue)
admin.site.register(Currency)
admin.site.register(Provider)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SpecialProposition)
admin.site.register(PreFilter, PreFilterAdmin)
admin.site.register(PreFilterParameterValue)
admin.site.register(ProductParameterAvailableInterval)
admin.site.register(DeliveryRule)
admin.site.register(Margin)
admin.site.register(Sale)
