from django.contrib import admin
from .models import Institution, Category

# Register your models here.

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    search_fields = ('name', 'type')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']