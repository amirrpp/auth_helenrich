from django.contrib import admin

# Models
from weblayout.models import *

# MPTT Tree View
from django_mptt_admin.admin import DjangoMpttAdmin


class MenuAdmin(DjangoMpttAdmin):
    pass


admin.site.register(Template)
admin.site.register(MainMenu, MenuAdmin)
admin.site.register(AdditionalMenu, MenuAdmin)
admin.site.register(ExtraMenu, MenuAdmin)
admin.site.register(SystemElement)
