from django.contrib import admin
from .models import Institution

# Register your models here.

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')  # Ustawiamy kolumny, które mają być widoczne w panelu
    search_fields = ('name', 'type')  # Dodajemy możliwość wyszukiwania po nazwie i typie instytucji