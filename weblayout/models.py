from django.db import models

# MPTT Modes and trees
from mptt.models import MPTTModel, TreeForeignKey

# Ckeditor support
from ckeditor.fields import RichTextField


class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    path = models.CharField(max_length=256, unique=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'templates'
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'


class MainMenu(MPTTModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', )
    url = models.CharField(max_length=256, default=None, null=True, blank=True)
    first_image = models.ImageField(
        upload_to="main_menu/", null=True, blank=True)
    second_image = models.ImageField(
        upload_to="main_menu/", null=True, blank=True)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'main_menu'
        verbose_name = 'Main Menu Element'
        verbose_name_plural = 'Main Menu'


class ExtraMenu(MPTTModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', )
    url = models.CharField(max_length=256, default=None, null=True, blank=True)
    first_image = models.ImageField(
        upload_to="extra_menu/", null=True, blank=True)
    second_image = models.ImageField(
        upload_to="extra_menu/", null=True, blank=True)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'extra_menu'
        verbose_name = 'Extra Menu Element'
        verbose_name_plural = 'Extra Menu'


class AdditionalMenu(MPTTModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    url = models.CharField(max_length=256, default=None, null=True, blank=True)
    first_image = models.ImageField(
        upload_to="additional_menu/", null=True, blank=True)
    second_image = models.ImageField(
        upload_to="additional_menu/", null=True, blank=True)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'additional_menu'
        verbose_name = 'Additional Menu Element'
        verbose_name_plural = 'Additional Menu'


class SystemElement(models.Model):
    ELEMENT_TYPE = (
        ('Header', 'Header'),
        ('Footer', 'Footer'),
        ('Script', 'Script')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, choices=ELEMENT_TYPE, unique=True)
    body = RichTextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'system_elements'
        verbose_name = 'System Element'
        verbose_name_plural = 'System Elements'
